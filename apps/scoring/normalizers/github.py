"""GitHub activity and project substance normalization."""

from datetime import datetime, timezone


def normalize_github(payload: dict) -> float:
    """Map repository activity consistency and project substance onto 0–100."""
    user = payload.get("user", {})
    repos = payload.get("repositories", [])
    count = max(0, int(user.get("public_repos", len(repos)) or 0))
    unique = [repo for repo in repos if not repo.get("fork")]
    recent = 0
    for repo in unique:
        try:
            age = (
                datetime.now(timezone.utc)
                - datetime.fromisoformat(repo["updated_at"].replace("Z", "+00:00"))
            ).days
            recent += age <= 365
        except (KeyError, TypeError, ValueError):
            continue
    activity = min(45, (recent / max(1, len(unique))) * 45)
    breadth = min(20, count * 2)
    substance = min(
        35,
        len(
            [
                r
                for r in unique
                if r.get("size", 0) >= 20
                and (
                    (r.get("description") or "").strip()
                    or len(r.get("readme", "")) >= 300
                )
            ]
        )
        * 5,
    )
    return round(min(100, activity + breadth + substance), 2)
