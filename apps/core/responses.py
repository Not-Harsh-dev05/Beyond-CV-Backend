"""Consistent API response envelopes."""

from typing import Any
from rest_framework.response import Response


def success(data: Any, *, status: int = 200, request=None, **meta: Any) -> Response:
    """Return a successful response with request-scoped metadata."""
    raw_request = getattr(request, "_request", request)
    return Response(
        {
            "success": True,
            "data": data,
            "meta": {
                "request_id": getattr(raw_request, "request_id", ""),
                "sources_used": meta.pop("sources_used", []),
                "sources_failed": meta.pop("sources_failed", []),
                "is_sample_data": meta.pop("is_sample_data", False),
                **meta,
            },
        },
        status=status,
    )


def failure(
    code: str, message: str, *, status: int = 400, request=None, details=None
) -> Response:
    """Return an error response without exposing implementation details."""
    raw_request = getattr(request, "_request", request)
    return Response(
        {
            "success": False,
            "error": {"code": code, "message": message, "details": details or {}},
            "meta": {"request_id": getattr(raw_request, "request_id", "")},
        },
        status=status,
    )
