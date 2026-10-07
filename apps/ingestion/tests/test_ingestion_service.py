"""Ingestion dedupe, cache, consent, and graceful degradation tests."""

from datetime import timedelta
import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APIClient
from apps.candidates.models import CandidateProfile, EvidenceLink
from apps.ingestion.models import IngestionJob, SignalSnapshot
from apps.ingestion.services import (
    build_competence_inputs,
    create_ingestion_job,
    collect_signals,
    process_candidate,
)
from apps.scoring.models import ScoreResult
from apps.scoring.competence import NoUsableSignals


def candidate(email, consent=True):
    user = get_user_model().objects.create_user(
        email=email, username=email.split("@")[0], password="StrongPass!234"
    )
    CandidateProfile.objects.create(user=user, consent_given=consent)
    return user


@pytest.mark.django_db
def test_competence_input_ignores_profile_and_raw_identity_fields():
    user = candidate("sanitize@example.test")
    profile = user.candidate_profile
    profile.name = "Ada Candidate"
    profile.gender = "PrivateGender"
    profile.region = "PrivateRegion"
    profile.college_tier = "TIER_1"
    profile.employer_brand = "PrivateEmployer"
    evidence = {
        "github": {
            "normalized": 70,
            "ownership_verified": True,
            "name": "Ignored Candidate Name",
            "gender": "Ignored Gender",
            "region": "Ignored Region",
            "college_tier": "Ignored Tier",
            "employer_brand": "Ignored Employer",
            "user": {"bio": "Ignored Candidate Name"},
            "repositories": [
                {
                    "name": "inventory-service",
                    "description": "Inventory orchestration service",
                    "readme": "A sufficiently detailed project README",
                    "fork": False,
                }
            ],
        }
    }
    isolated = build_competence_inputs(evidence)
    text = str(isolated)
    profile.name = "A Different Name"
    profile.gender = "DifferentGender"
    profile.region = "DifferentRegion"
    profile.college_tier = "TIER_2"
    profile.employer_brand = "DifferentEmployer"
    profile.save()
    assert str(build_competence_inputs(evidence)) == text
    for private_value in (
        "Ignored Candidate Name",
        "Ignored Gender",
        "Ignored Region",
        "Ignored Tier",
        "Ignored Employer",
    ):
        assert private_value not in text


@pytest.mark.django_db
def test_active_job_is_deduplicated():
    user = candidate("dedupe@example.test")
    first, created = create_ingestion_job(user)
    second, second_created = create_ingestion_job(user)
    assert created is True
    assert second_created is False
    assert first.pk == second.pk


@pytest.mark.django_db
def test_fresh_snapshot_avoids_refetch(monkeypatch):
    user = candidate("cache@example.test")
    link = EvidenceLink.objects.create(user=user, source="github", handle="cached")
    SignalSnapshot.objects.create(
        user=user,
        evidence_link=link,
        source="github",
        payload={
            "normalized": 61,
            "method": "api",
            "ownership_verified": True,
            "user": {"public_repos": 1},
            "repositories": [],
        },
        method="api",
        ttl=timedelta(hours=24),
        fetched_at=timezone.now(),
    )
    monkeypatch.setattr(
        "apps.ingestion.services.GitHubClient.fetch",
        lambda *_args: pytest.fail("fresh snapshot should be reused"),
    )
    signals, used, failed = collect_signals(user)
    assert used == ["github"] and not failed
    assert signals["github"]["normalized"] == 61


@pytest.mark.django_db
def test_multiple_links_from_one_source_are_aggregated(monkeypatch):
    user = candidate("multi-source@example.test")
    EvidenceLink.objects.create(user=user, source="github", handle="one")
    EvidenceLink.objects.create(user=user, source="github", handle="two")
    EvidenceLink.objects.create(user=user, source="github", handle="three")

    def fetch(_self, handle, _code):
        return {
            "user": {"public_repos": {"one": 1, "two": 1, "three": 10}[handle]},
            "repositories": [],
            "ownership_verified": True,
            "method": "api",
        }

    monkeypatch.setattr("apps.ingestion.services.GitHubClient.fetch", fetch)
    signals, used, failed = collect_signals(user)
    assert not failed
    assert used == ["github"]
    assert signals["github"]["normalized"] == 8


@pytest.mark.django_db
def test_force_refresh_bypasses_a_fresh_snapshot(monkeypatch):
    user = candidate("refresh@example.test")
    link = EvidenceLink.objects.create(user=user, source="github", handle="octocat")
    SignalSnapshot.objects.create(
        user=user,
        evidence_link=link,
        source="github",
        payload={
            "normalized": 10,
            "ownership_verified": False,
            "repositories": [],
        },
        method="api",
        ttl=timedelta(hours=24),
    )
    monkeypatch.setattr(
        "apps.ingestion.services.GitHubClient.fetch",
        lambda *_args: {
            "user": {"public_repos": 10},
            "repositories": [],
            "ownership_verified": True,
            "method": "api",
        },
    )

    cached, _, _ = collect_signals(user)
    assert cached["github"]["normalized"] == 10
    refreshed, _, failed = collect_signals(user, force_refresh=True)
    assert not failed
    assert refreshed["github"]["normalized"] == 20
    assert refreshed["github"]["ownership_verified"] is True


@pytest.mark.django_db
def test_successful_source_scores_while_unverifiable_source_is_reported_failed(
    monkeypatch,
):
    user = candidate("partial@example.test")
    EvidenceLink.objects.create(user=user, source="github", handle="live")
    EvidenceLink.objects.create(
        user=user, source="certificate", url="https://coursera.org/credential"
    )
    monkeypatch.setattr(
        "apps.ingestion.services.GitHubClient.fetch",
        lambda *_args: {
            "user": {"public_repos": 1},
            "repositories": [],
            "ownership_verified": False,
            "method": "api",
        },
    )
    monkeypatch.setattr(
        "apps.ingestion.services.CertificateClient.verify",
        lambda *_args: {
            "status": "unverifiable",
            "method": "scraped",
            "reason": "dynamic",
        },
    )
    result = process_candidate(user)
    assert result.sources_used == ["github"]
    assert result.sources_failed[0]["source"] == "certificate"
    assert result.competence >= 0


@pytest.mark.django_db
def test_no_successful_sources_never_returns_a_score(monkeypatch):
    user = candidate("empty@example.test")
    EvidenceLink.objects.create(
        user=user, source="certificate", url="https://coursera.org/no"
    )
    monkeypatch.setattr(
        "apps.ingestion.services.CertificateClient.verify",
        lambda *_args: {"status": "unverifiable", "method": "scraped"},
    )
    with pytest.raises(NoUsableSignals):
        process_candidate(user)
    assert not ScoreResult.objects.filter(user=user).exists()


@pytest.mark.django_db
def test_ingestion_api_requires_consent_and_returns_202_for_candidate(monkeypatch):
    user = candidate("apiingest@example.test", consent=False)
    client = APIClient()
    client.force_authenticate(user)
    denied = client.post("/api/v1/ingestion/jobs/", {}, format="json")
    assert denied.status_code == 403
    user.candidate_profile.consent_given = True
    user.candidate_profile.save()
    monkeypatch.setattr("apps.ingestion.views.run_ingestion.delay", lambda *_: None)
    response = client.post("/api/v1/ingestion/jobs/", {}, format="json")
    assert response.status_code == 202
    assert response.data["data"]["status"] == "PENDING"
    poll = client.get(f"/api/v1/ingestion/jobs/{response.data['data']['job_id']}/")
    assert poll.status_code == 200


@pytest.mark.django_db
def test_refresh_is_throttled_after_a_recent_success(monkeypatch):
    user = candidate("refresh-limit@example.test")
    IngestionJob.objects.create(
        user=user,
        dedupe_key="recent-success",
        status=IngestionJob.Status.SUCCESS,
        finished_at=timezone.now(),
    )
    client = APIClient()
    client.force_authenticate(user)

    response = client.post("/api/v1/ingestion/jobs/", {"refresh": True}, format="json")
    assert response.status_code == 429
    assert response.data["error"]["code"] == "refresh_too_soon"

    queued = []
    monkeypatch.setattr(
        "apps.ingestion.views.run_ingestion.delay",
        lambda *args: queued.append(args),
    )
    response = client.post("/api/v1/ingestion/jobs/", {}, format="json")
    assert response.status_code == 202
    assert queued == [(response.data["data"]["job_id"], False)]


@pytest.mark.django_db
def test_stale_active_job_does_not_block_a_new_ingestion():
    from django.test import override_settings

    user = candidate("stale@example.test")
    old_job, _ = create_ingestion_job(user)
    IngestionJob.objects.filter(pk=old_job.pk).update(
        created_at=timezone.now() - timedelta(hours=2)
    )

    with override_settings(INGESTION_STALE_MINUTES=30):
        new_job, created = create_ingestion_job(user)

    old_job.refresh_from_db()
    assert created and new_job.pk != old_job.pk
    assert old_job.status == IngestionJob.Status.FAILED
    assert "timed out" in old_job.error
