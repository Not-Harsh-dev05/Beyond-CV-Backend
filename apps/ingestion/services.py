"""Orchestrate live evidence acquisition, caching, and score computation."""

import logging
import uuid
from django.contrib.auth import get_user_model
from datetime import timedelta
import httpx
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from apps.core.utils import stable_key
from apps.candidates.models import EvidenceLink, CandidateProfile
from apps.scoring.competence import CompetenceScorer, NoUsableSignals
from apps.scoring.pedigree import PedigreeBaseline
from apps.scoring.delta import calculate_delta
from apps.scoring.models import ScoreResult
from apps.scoring.normalizers.github import normalize_github
from apps.scoring.normalizers.kaggle import normalize_kaggle
from apps.scoring.normalizers.certificates import normalize_certificate
from .models import IngestionJob, SignalSnapshot
from .clients.github_client import GitHubClient
from .clients.kaggle_client import KaggleClient
from .clients.certificate_client import CertificateClient

logger = logging.getLogger(__name__)


def reap_stale_jobs(user=None) -> int:
    """Fail active ingestion jobs that have been stuck longer than allowed."""
    cutoff = timezone.now() - timedelta(minutes=settings.INGESTION_STALE_MINUTES)
    stale = IngestionJob.objects.filter(
        status__in=[IngestionJob.Status.PENDING, IngestionJob.Status.RUNNING],
        created_at__lt=cutoff,
    )
    if user is not None:
        stale = stale.filter(user=user)
    return stale.update(
        status=IngestionJob.Status.FAILED,
        error="Job timed out and was marked failed; please retry.",
        finished_at=timezone.now(),
    )


def create_ingestion_job(user) -> tuple[IngestionJob, bool]:
    """Create or reuse the user's active ingestion job."""
    key = stable_key(str(user.pk), str(uuid.uuid4()))
    reap_stale_jobs(user)
    with transaction.atomic():
        get_user_model().objects.select_for_update().get(pk=user.pk)
        active = (
            IngestionJob.objects.select_for_update()
            .filter(
                user=user,
                status__in=[IngestionJob.Status.PENDING, IngestionJob.Status.RUNNING],
            )
            .first()
        )
        if active:
            return active, False
        job, created = IngestionJob.objects.get_or_create(
            dedupe_key=key, defaults={"user": user}
        )
        return job, created


def _merge_payloads(source: str, items: list[dict]) -> dict:
    """Combine multiple evidence links for one source using their arithmetic mean."""
    if len(items) == 1:
        return items[0]
    combined = dict(items[0])
    combined["normalized"] = round(
        sum(float(item["normalized"]) for item in items) / len(items), 2
    )
    combined["ownership_verified"] = all(
        bool(item.get("ownership_verified")) for item in items
    )
    if source == EvidenceLink.Source.GITHUB:
        combined["repositories"] = [
            repo for item in items for repo in item.get("repositories", [])
        ]
    if source == EvidenceLink.Source.CERTIFICATE:
        combined["status"] = (
            "verified"
            if all(item.get("status") == "verified" for item in items)
            else "unverifiable"
        )
    return combined


def collect_signals(
    user, force_refresh: bool = False
) -> tuple[dict, list[str], list[dict]]:
    """Fetch/cache each available source and report failures individually."""
    per_source, used, failed = {}, [], []
    links = user.evidence_links.all()
    for link in links:
        cached = None
        if not force_refresh:
            cached = (
                SignalSnapshot.objects.filter(
                    user=user, source=link.source, evidence_link=link
                )
                .order_by("-fetched_at")
                .first()
            )
        if cached and cached.fresh:
            payload = cached.payload
        else:
            try:
                if link.source == EvidenceLink.Source.GITHUB:
                    payload = GitHubClient().fetch(link.handle, link.verification_code)
                    payload["ownership_verified"] = bool(
                        payload.get("ownership_verified") or link.ownership_verified
                    )
                    if payload["ownership_verified"] and not link.ownership_verified:
                        link.ownership_verified = True
                        link.save(update_fields=("ownership_verified",))
                    normalized = normalize_github(payload)
                elif link.source == EvidenceLink.Source.KAGGLE:
                    payload = KaggleClient().fetch(link.handle)
                    normalized = normalize_kaggle(payload)
                else:
                    payload = CertificateClient().verify(link.url)
                    normalized = normalize_certificate(payload)
                payload["normalized"] = normalized
                SignalSnapshot.objects.create(
                    user=user,
                    evidence_link=link,
                    source=link.source,
                    payload=payload,
                    method=payload.get("method", "api"),
                    ttl=timedelta(hours=settings.SIGNAL_TTL_HOURS),
                )
            except (
                httpx.HTTPError,
                RuntimeError,
                ValueError,
                OSError,
                KeyError,
                TypeError,
            ) as exc:
                logger.warning(
                    "source_fetch_failed source=%s user_id=%s error=%s",
                    link.source,
                    user.pk,
                    str(exc)[:200],
                )
                failed.append({"source": link.source, "reason": str(exc)[:200]})
                continue
        if "normalized" not in payload:
            if link.source == EvidenceLink.Source.GITHUB:
                payload["normalized"] = normalize_github(payload)
            elif link.source == EvidenceLink.Source.KAGGLE:
                payload["normalized"] = normalize_kaggle(payload)
            else:
                payload["normalized"] = normalize_certificate(payload)
        if payload.get("normalized") is None:
            failed.append(
                {"source": link.source, "reason": "Evidence could not be verified."}
            )
            continue
        payload["ownership_verified"] = bool(
            payload.get("ownership_verified") or link.ownership_verified
        )
        per_source.setdefault(link.source, []).append(payload)
        if link.source not in used:
            used.append(link.source)
    signals = {
        source: _merge_payloads(source, items) for source, items in per_source.items()
    }
    return signals, used, failed


def build_competence_inputs(signals: dict) -> dict:
    """Project raw snapshots to an allowlisted evidence-only scorer input."""
    competence_inputs = {}
    for source, payload in signals.items():
        evidence = {
            "normalized": payload.get("normalized"),
            "ownership_verified": bool(payload.get("ownership_verified")),
        }
        if source == "certificate":
            evidence["status"] = payload.get("status")
        if source == "github":
            evidence["projects"] = [
                {
                    "name": str(repo.get("name", "")),
                    "description": str(repo.get("description", "")),
                    "readme": str(repo.get("readme", "")),
                    "fork": bool(repo.get("fork")),
                }
                for repo in payload.get("repositories", [])
            ]
        competence_inputs[source] = evidence
    return competence_inputs


def process_candidate(
    user, *, is_sample_data=False, ingestion_job=None, force_refresh=False
) -> ScoreResult:
    """Compute and persist a score from at least one successfully fetched evidence source."""
    profile = CandidateProfile.objects.get(user=user)
    if profile.is_sample_data:
        raise PermissionError(
            "Synthetic demo evidence cannot be processed as live evidence."
        )
    if not profile.consent_given:
        raise PermissionError("Candidate consent is required before ingestion.")
    signals, used, failed = collect_signals(user, force_refresh=force_refresh)
    if not signals:
        raise NoUsableSignals("No evidence sources were successfully fetched.")
    competence_inputs = build_competence_inputs(signals)
    competence = CompetenceScorer().score(competence_inputs)
    baseline = PedigreeBaseline().predict(profile.college_tier, profile.employer_brand)
    delta = calculate_delta(competence["score"], baseline["score"])
    ownership = all(
        (source == "certificate" and item.get("status") == "verified")
        or bool(item.get("ownership_verified"))
        for source, item in signals.items()
    )
    values = dict(
        user=user,
        competence=competence["score"],
        baseline=baseline["score"],
        delta=delta,
        baseline_source=baseline["source"],
        warning=baseline.get("warning", ""),
        breakdown=competence["breakdown"],
        sources_used=used,
        sources_failed=failed,
        ownership_verified=ownership,
        is_sample_data=is_sample_data,
    )
    if ingestion_job is not None:
        result, _ = ScoreResult.objects.update_or_create(
            ingestion_job=ingestion_job, defaults=values
        )
        return result
    return ScoreResult.objects.create(**values)
