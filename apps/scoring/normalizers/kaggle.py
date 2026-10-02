"""Competition percentile normalization."""

from math import isfinite


def normalize_kaggle(payload: dict) -> float:
    """Convert explicit percentile or leaderboard position into a 0–100 score."""
    if "percentile" in payload:
        percentile = float(payload["percentile"])
        if not isfinite(percentile):
            raise ValueError("Kaggle percentile must be finite.")
        return round(max(0.0, min(100.0, percentile)), 2)
    rows = payload.get("leaderboard", [])
    if not isinstance(rows, list) or not rows:
        raise ValueError("Kaggle leaderboard contains no usable entries.")
    target = payload.get("username", "").lower()
    ranks = [
        i
        for i, row in enumerate(rows)
        if str(row.get("teamName", "")).lower() == target
    ]
    if not ranks:
        raise ValueError("Candidate was not found on the supplied leaderboard.")
    return round(100 * (1 - ranks[0] / max(1, len(rows) - 1)), 2)
