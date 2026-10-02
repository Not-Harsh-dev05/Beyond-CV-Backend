"""Privacy-preserving aggregates for undervalued evidence skill categories."""

from collections import defaultdict
from django.conf import settings
from apps.candidates.models import CandidateProfile
from apps.ingestion.models import SignalSnapshot
from apps.scoring.models import ScoreResult


def undervalued_skills(region: str = "", tier: str = "") -> list[dict]:
    """Aggregate positive-delta GitHub language signals and suppress small groups."""
    groups = defaultdict(lambda: {"count": 0, "delta_sum": 0.0})
    profiles = CandidateProfile.objects.filter(consent_given=True)
    if region:
        profiles = profiles.filter(region__iexact=region)
    if tier:
        profiles = profiles.filter(college_tier=tier)
    for profile in profiles:
        score = (
            ScoreResult.objects.filter(user=profile.user)
            .order_by("-computed_at")
            .first()
        )
        if (
            not score
            or score.is_sample_data
            or profile.is_sample_data
            or score.delta <= 0
        ):
            continue
        language_names = set()
        for snapshot in SignalSnapshot.objects.filter(
            user=profile.user, source="github"
        ):
            language_names.update(
                repo.get("language")
                for repo in snapshot.payload.get("repositories", [])
                if repo.get("language")
            )
        for language in language_names:
            key = (language, profile.region or "Unknown", profile.college_tier)
            groups[key]["count"] += 1
            groups[key]["delta_sum"] += score.delta
    result = []
    for (skill, group_region, group_tier), aggregate in groups.items():
        if aggregate["count"] < settings.INSIGHTS_MIN_GROUP_SIZE:
            continue
        result.append(
            {
                "skill_category": skill,
                "region": group_region,
                "tier": group_tier,
                "candidate_count": aggregate["count"],
                "average_delta": round(aggregate["delta_sum"] / aggregate["count"], 2),
            }
        )
    return sorted(result, key=lambda item: item["average_delta"], reverse=True)
