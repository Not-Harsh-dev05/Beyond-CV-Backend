"""Ownership and consent enforcement for candidate routes."""

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.candidates.models import CandidateProfile, EvidenceLink
from apps.scoring.models import ScoreResult
from apps.ingestion.models import SignalSnapshot
from datetime import timedelta


def make_user(email, role="CANDIDATE"):
    return get_user_model().objects.create_user(
        email=email, username=email.split("@")[0], password="StrongPass!234", role=role
    )


@pytest.mark.django_db
def test_candidate_cannot_read_another_candidate_score_or_evidence():
    first, second = make_user("a@example.test"), make_user("b@example.test")
    CandidateProfile.objects.create(user=first, consent_given=True)
    CandidateProfile.objects.create(user=second, consent_given=True)
    EvidenceLink.objects.create(user=second, source="github", handle="another")
    client = APIClient()
    client.force_authenticate(first)
    response = client.get(f"/api/v1/candidates/{second.pk}/score/")
    assert response.status_code == 404
    evidence = client.post(
        "/api/v1/candidates/me/evidence/",
        {"source": "github", "handle": "first"},
        format="json",
    )
    assert evidence.status_code == 201
    assert EvidenceLink.objects.filter(user=first).count() == 1
    assert evidence.data["data"]["verification_code"]


@pytest.mark.django_db
def test_candidate_can_delete_own_account_and_related_profile():
    user = make_user("delete@example.test")
    CandidateProfile.objects.create(user=user)
    EvidenceLink.objects.create(user=user, source="github", handle="delete-me")
    client = APIClient()
    client.force_authenticate(user)
    response = client.delete("/api/v1/candidates/me/")
    assert response.status_code == 200
    assert not get_user_model().objects.filter(pk=user.pk).exists()
    assert not CandidateProfile.objects.filter(user_id=user.pk).exists()


@pytest.mark.django_db
def test_recruiter_can_see_only_consenting_candidate_score():
    candidate = make_user("consenting@example.test")
    recruiter = make_user("viewer@example.test", "RECRUITER")
    CandidateProfile.objects.create(user=candidate, consent_given=True)
    ScoreResult.objects.create(
        user=candidate,
        competence=75,
        baseline=50,
        delta=25,
        baseline_source="sample_synthetic",
        warning="sample baseline",
        breakdown={"github": {"score": 75}},
        sources_used=["github"],
        sources_failed=[],
        ownership_verified=False,
        is_sample_data=False,
    )
    client = APIClient()
    client.force_authenticate(recruiter)
    response = client.get(f"/api/v1/candidates/{candidate.pk}/score/")
    assert response.status_code == 200
    assert response.data["data"]["delta"] == 25
    candidate.candidate_profile.consent_given = False
    candidate.candidate_profile.save()
    denied = client.get(f"/api/v1/candidates/{candidate.pk}/score/")
    assert denied.status_code == 404


@pytest.mark.django_db
def test_candidate_profile_and_evidence_edit_are_owner_scoped():
    first, second = make_user("edit-a@example.test"), make_user("edit-b@example.test")
    CandidateProfile.objects.create(user=first, consent_given=True)
    own_link = EvidenceLink.objects.create(
        user=first, source="github", handle="before", verification_code="challenge"
    )
    other_link = EvidenceLink.objects.create(
        user=second, source="github", handle="private"
    )
    SignalSnapshot.objects.create(
        user=first,
        evidence_link=own_link,
        source="github",
        payload={"normalized": 1},
        method="api",
        ttl=timedelta(days=1),
    )
    client = APIClient()
    client.force_authenticate(first)
    profile = client.get("/api/v1/candidates/me/")
    assert profile.status_code == 200
    updated = client.put(
        "/api/v1/candidates/me/",
        {"name": "Candidate A", "consent_given": True},
        format="json",
    )
    assert updated.status_code == 200
    forbidden = client.patch(
        f"/api/v1/candidates/me/evidence/{other_link.pk}/",
        {"handle": "steal"},
        format="json",
    )
    assert forbidden.status_code == 403
    patched = client.patch(
        f"/api/v1/candidates/me/evidence/{own_link.pk}/",
        {"handle": "after"},
        format="json",
    )
    assert patched.status_code == 200
    own_link.refresh_from_db()
    assert own_link.ownership_verified is False
    assert own_link.verification_code
    assert not own_link.snapshots.exists()
    deleted = client.delete(f"/api/v1/candidates/me/evidence/{own_link.pk}/")
    assert deleted.status_code == 200


@pytest.mark.django_db
def test_seeded_demo_responses_are_explicitly_sample_marked():
    from django.core.management import call_command

    call_command("seed_demo_data", verbosity=0)
    candidate = get_user_model().objects.get(email="demo.candidate@example.test")
    recruiter = get_user_model().objects.get(email="demo.recruiter@example.test")
    client = APIClient()
    client.force_authenticate(candidate)
    login = client.post(
        "/api/v1/auth/login/",
        {"email": candidate.email, "password": "DemoCandidate!234"},
        format="json",
    )
    assert login.data["meta"]["is_sample_data"] is True
    profile = client.get("/api/v1/candidates/me/")
    assert profile.data["meta"]["is_sample_data"] is True
    score = client.get(f"/api/v1/candidates/{candidate.pk}/score/")
    assert score.data["meta"]["is_sample_data"] is True
    assert score.data["data"]["is_sample_data"] is True
    assert client.post("/api/v1/ingestion/jobs/", {}, format="json").status_code == 403
    client.force_authenticate(recruiter)
    jobs = client.get("/api/v1/jobs/")
    assert jobs.data["meta"]["is_sample_data"] is True
