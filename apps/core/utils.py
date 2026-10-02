"""Small shared utilities."""

import hashlib


def stable_key(*parts: str) -> str:
    """Return an opaque deterministic deduplication key."""
    return hashlib.sha256(":".join(parts).encode("utf-8")).hexdigest()
