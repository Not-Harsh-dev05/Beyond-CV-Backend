"""Candidate fit, delta normalization, and explainable ranking generation."""

import re

from django.conf import settings
from apps.candidates.models import CandidateProfile
from apps.ingestion.models import SignalSnapshot
from apps.scoring.models import ScoreResult


def rank_candidates(job) -> list[dict]:
    """Rank consenting candidates with both role-fit and normalized delta factors."""
    required = [skill.lower() for skill in job.required_skills]
    weights = {key.lower(): float(value) for key, value in job.skill_weights.items()}
    candidates = CandidateProfile.objects.filter(consent_given=True).select_related(
        "user"
    )
    entries = []
    for profile in candidates:
        score = (
            ScoreResult.objects.filter(user=profile.user)
            .order_by("-computed_at")
            .first()
        )
        if not score:
            continue
        snapshots = SignalSnapshot.objects.filter(user=profile.user)
        corpus = []
        for snap in snapshots:
            payload = snap.payload
            corpus.append(str(payload.get("user", {}).get("bio", "")))
            for repo in payload.get("repositories", []):
                corpus.extend(
                    [
                        str(repo.get("name", "")),
                        str(repo.get("description", "")),
                        str(repo.get("language", "")),
                    ]
                )
        evidence_text = " ".join(corpus).lower()
        matched = [
            skill
            for skill in required
            if re.search(rf"(?<!\w){re.escape(skill)}(?!\w)", evidence_text)
        ]
        total_weight = sum(weights.get(skill, 1.0) for skill in required)
        role_fit = (
            sum(weights.get(skill, 1.0) for skill in matched) / total_weight * 100
            if required and total_weight > 0
            else 0.0
        )
        normalized_delta = max(0.0, min(100.0, (score.delta + 100.0) / 2.0))
        ranking_score = (
            settings.RANKING_W_FIT * role_fit
            + settings.RANKING_W_DELTA * normalized_delta
        )
        sources = list(score.sources_used)
        driver = ", ".join(sources) if sources else "available evidence"
        rationale = (
            f"Candidate shows a {score.delta:+.0f} competence delta over the pedigree baseline, "
            f"with evidence from {driver}. Matched {len(matched)} of {len(required)} required skills."
        )
        entries.append(
            {
                "candidate_id": profile.user_id,
                "competence": score.competence,
                "baseline": score.baseline,
                "delta": score.delta,
                "baseline_source": score.baseline_source,
                "baseline_warning": score.warning,
                "role_fit": round(role_fit, 2),
                "normalized_delta": round(normalized_delta, 2),
                "ranking_score": round(ranking_score, 2),
                "matched_skills": matched,
                "required_skills": job.required_skills,
                "evidence_breakdown": score.breakdown,
                "sources_used": score.sources_used,
                "sources_failed": score.sources_failed,
                "ownership_verified": score.ownership_verified,
                "rationale": rationale,
                "is_sample_data": score.is_sample_data
                or profile.is_sample_data
                or job.is_sample_data,
            }
        )
    return sorted(entries, key=lambda row: row["ranking_score"], reverse=True)
