"""Evidence-only competence scoring; pedigree fields are intentionally excluded."""

from math import isfinite, sqrt
from django.conf import settings
from .embeddings import get_embedding_service

SOURCE_KEYS = frozenset({"github", "kaggle", "certificate"})
SIGNAL_FIELDS = frozenset({"normalized", "ownership_verified", "status", "projects"})


class NoUsableSignals(ValueError):
    """Raised when no successfully normalized evidence exists."""


class CompetenceScorer:
    """Score only source signals, with unverified ownership discounted."""

    def __init__(self, embedder=None):
        self.embedder = embedder

    def score(self, signals: dict) -> dict:
        """Produce a 0–100 competence score and explainable source breakdown."""
        if not isinstance(signals, dict) or set(signals) - SOURCE_KEYS:
            raise ValueError("CompetenceScorer accepts evidence-source signals only.")
        if any(
            not isinstance(payload, dict) or set(payload) - SIGNAL_FIELDS
            for payload in signals.values()
        ):
            raise ValueError(
                "CompetenceScorer accepts only normalized evidence fields."
            )
        effective, breakdown = [], {}
        for source, payload in signals.items():
            value = payload.get("normalized")
            if value is None:
                continue
            score = float(value)
            if not isfinite(score):
                raise ValueError("Evidence scores must be finite numeric values.")
            score = max(0.0, min(100.0, score))
            verified = (
                source == "certificate"
                and payload.get("status") == "verified"
                or bool(payload.get("ownership_verified"))
            )
            weight = 1.0 if verified else settings.UNVERIFIED_SIGNAL_WEIGHT
            if weight <= 0:
                breakdown[source] = {
                    "score": round(score, 2),
                    "weight": 0.0,
                    "ownership_verified": verified,
                    "detail": payload.get("explanation", ""),
                }
                continue
            effective.append((score, weight))
            breakdown[source] = {
                "score": round(score, 2),
                "weight": weight,
                "ownership_verified": verified,
                "detail": payload.get("explanation", ""),
            }
        if not effective:
            raise NoUsableSignals("No successfully normalized evidence was supplied.")
        score = sum(value * weight for value, weight in effective) / sum(
            weight for _, weight in effective
        )
        github = signals.get("github", {})
        projects = github.get("projects", [])
        if projects:
            embedder = self.embedder or get_embedding_service()
            tutorials = (
                "tutorial",
                "course project",
                "bootcamp",
                "followed along",
                "starter template",
                "clone of",
                "from the course",
                "assignment",
            )
            substantive = [
                p
                for p in projects
                if not p.get("fork")
                and not any(
                    marker in f"{p.get('name', '')} {p.get('description', '')} "
                    f"{p.get('readme', '')[:1000]}".lower()
                    for marker in tutorials
                )
                and (
                    len(p.get("readme", "")) >= 300
                    or len(p.get("description", "")) >= 20
                )
            ]
            docs = [
                f"{p.get('name', '')} {p.get('description', '')} {p.get('readme', '')[:4000]}"
                for p in substantive
            ]
            semantic = 0.0
            if docs:
                vectors = embedder.embed(docs)
                semantic = sum(
                    sqrt(sum(component * component for component in vector))
                    for vector in vectors
                ) / len(vectors)
            substance_bonus = min(6.0, len(substantive) * 1.5 + semantic * 0.05)
            score = min(100.0, score + substance_bonus)
            breakdown["project_substance"] = {
                "bonus": round(substance_bonus, 2),
                "project_count": len(substantive),
                "excluded_as_tutorial_or_fork": len(projects) - len(substantive),
            }
        return {"score": round(score, 2), "breakdown": breakdown}
