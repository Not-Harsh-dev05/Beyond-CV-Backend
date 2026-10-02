"""Prove profile pedigree and identity mutations do not affect competence."""

import pytest
from django.contrib.auth import get_user_model
from apps.candidates.models import CandidateProfile
from apps.scoring.competence import CompetenceScorer
from apps.scoring.embeddings import StubEmbeddingService


@pytest.mark.django_db
def test_identity_and_pedigree_mutations_do_not_change_competence():
    user = get_user_model().objects.create_user(
        email="isolation@example.test", username="isolation", password="Secret!12345"
    )
    profile = CandidateProfile.objects.create(
        user=user,
        name="First",
        gender="x",
        region="North",
        college_tier="TIER_1",
        employer_brand="Brand",
    )
    evidence = {
        "github": {"normalized": 81, "ownership_verified": True, "projects": []}
    }
    scorer = CompetenceScorer(embedder=StubEmbeddingService())
    original = scorer.score(evidence)["score"]
    for field, value in (
        ("college_tier", "TIER_3"),
        ("employer_brand", "Other"),
        ("name", "Changed"),
        ("gender", "y"),
        ("region", "South"),
    ):
        setattr(profile, field, value)
        profile.save()
        assert scorer.score(evidence)["score"] == original
