"""Unit coverage for source scales, scorer guards, delta and baseline fallback."""

import pandas as pd
import pytest
from django.test import override_settings
from apps.scoring.competence import CompetenceScorer, NoUsableSignals
from apps.scoring.delta import calculate_delta
from apps.scoring.embeddings import StubEmbeddingService
from apps.scoring.normalizers.github import normalize_github
from apps.scoring.normalizers.kaggle import normalize_kaggle
from apps.scoring.normalizers.certificates import normalize_certificate
from apps.scoring.pedigree import PedigreeBaseline, train_model


def test_delta_is_pure_and_clamped_only_by_input():
    assert calculate_delta(75, 40) == 35
    assert calculate_delta(0, 100) == -100
    assert calculate_delta(49.125, 50) == -0.88


def test_github_normalizer_and_malformed_dates():
    payload = {
        "user": {"public_repos": 1},
        "repositories": [
            {
                "fork": False,
                "size": 100,
                "description": "substantial",
                "updated_at": "not-a-date",
            }
        ],
    }
    assert normalize_github(payload) == 7
    assert normalize_github({"user": {}, "repositories": []}) == 0


def test_kaggle_percentile_clamps_and_leaderboard_position():
    assert normalize_kaggle({"percentile": 105}) == 100
    assert (
        normalize_kaggle(
            {
                "username": "team-a",
                "leaderboard": [
                    {"teamName": "team-a"},
                    {"teamName": "team-b"},
                    {"teamName": "team-c"},
                ],
            }
        )
        == 100
    )
    with pytest.raises(ValueError):
        normalize_kaggle({"leaderboard": []})


def test_certificate_only_scores_explicit_verification():
    assert normalize_certificate({"status": "unverifiable"}) is None
    assert (
        normalize_certificate(
            {
                "status": "verified",
                "title": "Advanced course",
                "text_excerpt": "x" * 100,
            }
        )
        == 25
    )


def test_competence_only_accepts_allowlisted_normalized_evidence():
    scorer = CompetenceScorer(embedder=StubEmbeddingService())
    result = scorer.score(
        {"github": {"normalized": 80, "ownership_verified": False, "projects": []}}
    )
    assert result["score"] == 80
    with pytest.raises(ValueError):
        scorer.score({"college_tier": {"normalized": 70}})
    with pytest.raises(ValueError):
        scorer.score({"github": {"normalized": 70, "name": "candidate"}})
    with pytest.raises(NoUsableSignals):
        scorer.score({"certificate": {"normalized": None, "status": "unverifiable"}})


def test_project_substance_filters_tutorials_and_uses_stub_embedder():
    result = CompetenceScorer(embedder=StubEmbeddingService()).score(
        {
            "github": {
                "normalized": 60,
                "ownership_verified": True,
                "projects": [
                    {
                        "name": "course-project",
                        "description": "followed along tutorial",
                        "readme": "",
                        "fork": False,
                    },
                    {
                        "name": "inventory-engine",
                        "description": "Production inventory management engine",
                        "readme": "Detailed architecture and implementation. " * 12,
                        "fork": False,
                    },
                ],
            }
        }
    )
    assert result["breakdown"]["project_substance"]["project_count"] == 1
    assert result["breakdown"]["project_substance"]["excluded_as_tutorial_or_fork"] == 1
    assert result["score"] > 60


def test_unverified_signals_have_configured_weight():
    with override_settings(UNVERIFIED_SIGNAL_WEIGHT=0.2):
        score = CompetenceScorer(embedder=StubEmbeddingService()).score(
            {
                "github": {"normalized": 0, "ownership_verified": False},
                "kaggle": {"normalized": 100, "ownership_verified": True},
            }
        )
    assert score["score"] == pytest.approx(83.33, abs=0.01)


def test_pedigree_falls_back_to_sample_and_trains_from_only_allowed_fields(tmp_path):
    baseline = PedigreeBaseline(tmp_path / "missing.joblib").predict(
        "TIER_1", "Large enterprise"
    )
    assert baseline["source"] == "sample_synthetic"
    assert "synthetic" in baseline["warning"].lower()
    csv = tmp_path / "train.csv"
    pd.DataFrame(
        {
            "college_tier": ["TIER_1", "TIER_3"],
            "employer_brand": ["X", "Y"],
            "competence": [70, 40],
            "region": ["A", "B"],
        }
    ).to_csv(csv, index=False)
    artifact = train_model(str(csv), str(tmp_path / "model.joblib"))
    assert (
        PedigreeBaseline(artifact).predict("TIER_1", "X")["source"] == "trained_model"
    )
    pd.DataFrame({"region": ["A"]}).to_csv(csv, index=False)
    with pytest.raises(ValueError):
        train_model(str(csv), str(tmp_path / "bad.joblib"))
