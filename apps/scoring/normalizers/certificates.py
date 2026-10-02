"""Verified certificate depth normalization."""


def normalize_certificate(payload: dict) -> float | None:
    """Assign a conservative evidence score only to parsed verified credentials."""
    if payload.get("status") != "verified":
        return None
    text = f"{payload.get('title', '')} {payload.get('text_excerpt', '')}".lower()
    return float(min(70, 20 + min(40, len(text) // 20)))
