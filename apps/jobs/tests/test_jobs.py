"""Job creation role authorization."""

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.jobs.models import JobRole


def user(email, role):
    return get_user_model().objects.create_user(
        email=email, username=email.split("@")[0], password="StrongPass!234", role=role
    )


@pytest.mark.django_db
def test_recruiter_can_create_role_candidate_cannot():
    recruiter, candidate = user("recruiter@example.test", "RECRUITER"), user(
        "candidate@example.test", "CANDIDATE"
    )
    client = APIClient()
    client.force_authenticate(recruiter)
    response = client.post(
        "/api/v1/jobs/",
        {"title": "Engineer", "required_skills": ["Python"]},
        format="json",
    )
    assert response.status_code == 201
    assert JobRole.objects.get().recruiter == recruiter
    client.force_authenticate(candidate)
    denied = client.post(
        "/api/v1/jobs/", {"title": "Nope", "required_skills": ["Python"]}, format="json"
    )
    assert denied.status_code == 403
