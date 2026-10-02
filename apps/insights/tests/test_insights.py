"""k-anonymous aggregates and role access tests."""

from datetime import timedelta
import pytest
from django.contrib.auth import get_user_model
from django.test import override_settings
from rest_framework.test import APIClient
from apps.candidates.models import CandidateProfile
from apps.ingestion.models import SignalSnapshot
from apps.scoring.models import ScoreResult
from apps.insights.services import undervalued_skills


@pytest.mark.django_db
@override_settings(INSIGHTS_MIN_GROUP_SIZE=5)
def test_insights_suppress_groups_below_k_and_return_only_aggregates():
    user_model = get_user_model()
    for index in range(5):
        user = user_model.objects.create_user(
            email=f"agg{index}@example.test",
            username=f"agg{index}",
            password="StrongPass!234",
        )
        CandidateProfile.objects.create(
            user=user, consent_given=True, region="South", college_tier="TIER_3"
        )
        ScoreResult.objects.create(
            user=user,
            competence=80,
            baseline=50,
            delta=30,
            baseline_source="sample_synthetic",
            breakdown={},
        )
        SignalSnapshot.objects.create(
            user=user,
            source="github",
            method="api",
            ttl=timedelta(days=1),
            payload={"repositories": [{"language": "Python"}]},
        )
    hidden = user_model.objects.create_user(
        email="agg-hidden@example.test",
        username="agg-hidden",
        password="StrongPass!234",
    )
    CandidateProfile.objects.create(
        user=hidden, consent_given=True, region="South", college_tier="TIER_3"
    )
    ScoreResult.objects.create(
        user=hidden,
        competence=90,
        baseline=40,
        delta=50,
        baseline_source="sample_synthetic",
        breakdown={},
    )
    SignalSnapshot.objects.create(
        user=hidden,
        source="github",
        method="api",
        ttl=timedelta(days=1),
        payload={"repositories": [{"language": "Rust"}]},
    )
    data = undervalued_skills(region="South", tier="TIER_3")
    assert len(data) == 1
    assert data[0]["skill_category"] == "Python"
    assert data[0]["candidate_count"] == 5
    assert "candidate_id" not in data[0]


@pytest.mark.django_db
def test_insights_are_admin_only():
    user = get_user_model().objects.create_user(
        email="notadmin@example.test", username="notadmin", password="StrongPass!234"
    )
    client = APIClient()
    client.force_authenticate(user)
    response = client.get("/api/v1/insights/undervalued-skills/")
    assert response.status_code == 403


@pytest.mark.django_db
def test_admin_can_request_aggregate_insights():
    user = get_user_model().objects.create_user(
        email="admininsight@example.test",
        username="admininsight",
        password="StrongPass!234",
        role="ADMIN",
    )
    client = APIClient()
    client.force_authenticate(user)
    response = client.get("/api/v1/insights/undervalued-skills/")
    assert response.status_code == 200
    assert response.data["success"] is True
