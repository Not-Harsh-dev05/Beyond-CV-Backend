"""Consent filtering and interpretable ranking formula tests."""

from datetime import timedelta
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.candidates.models import CandidateProfile
from apps.ingestion.models import SignalSnapshot
from apps.jobs.models import JobRole
from apps.scoring.models import ScoreResult
from apps.ranking.services import rank_candidates


def create_user(email, role):
    return get_user_model().objects.create_user(
        email=email, username=email.split("@")[0], password="StrongPass!234", role=role
    )


@pytest.mark.django_db
def test_rank_formula_returns_evidence_and_excludes_nonconsenting_candidates():
    recruiter = create_user("rank.recruiter@example.test", "RECRUITER")
    candidate = create_user("rank.candidate@example.test", "CANDIDATE")
    hidden = create_user("hidden.candidate@example.test", "CANDIDATE")
    CandidateProfile.objects.create(user=candidate, consent_given=True)
    CandidateProfile.objects.create(user=hidden, consent_given=False)
    role = JobRole.objects.create(
        recruiter=recruiter,
        title="Data engineer",
        required_skills=["Python", "SQL"],
        skill_weights={"Python": 2, "SQL": 1},
    )
    ScoreResult.objects.create(
        user=candidate,
        competence=80,
        baseline=40,
        delta=40,
        baseline_source="sample_synthetic",
        breakdown={"github": {"score": 80}},
        sources_used=["github"],
        ownership_verified=True,
    )
    ScoreResult.objects.create(
        user=hidden,
        competence=99,
        baseline=20,
        delta=79,
        baseline_source="sample_synthetic",
        breakdown={},
        sources_used=["github"],
    )
    SignalSnapshot.objects.create(
        user=candidate,
        source="github",
        method="api",
        ttl=timedelta(days=1),
        payload={
            "repositories": [
                {
                    "name": "python-service",
                    "description": "SQL backend",
                    "language": "Python",
                }
            ]
        },
    )
    rows = rank_candidates(role)
    assert len(rows) == 1
    assert rows[0]["matched_skills"] == ["python", "sql"]
    assert rows[0]["ranking_score"] == pytest.approx(91.0)
    assert rows[0]["sources_used"] == ["github"]
    assert rows[0]["rationale"]


@pytest.mark.django_db
def test_recruiter_rank_endpoint_and_candidate_denial():
    recruiter = create_user("ranking@example.test", "RECRUITER")
    candidate = create_user("not-recruiter@example.test", "CANDIDATE")
    job = JobRole.objects.create(
        recruiter=recruiter, title="Role", required_skills=["Python"]
    )
    client = APIClient()
    client.force_authenticate(recruiter)
    assert client.get(f"/api/v1/jobs/{job.pk}/ranking/").status_code == 200
    client.force_authenticate(candidate)
    assert client.get(f"/api/v1/jobs/{job.pk}/ranking/").status_code == 403
