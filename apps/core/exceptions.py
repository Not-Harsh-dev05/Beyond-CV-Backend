"""REST exception mapping to the standard API envelope."""

import logging
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def api_exception_handler(exc, context):
    """Convert known DRF errors to a stable envelope; keep server errors opaque."""
    response = exception_handler(exc, context)
    request = context.get("request")
    request_id = getattr(request, "request_id", "")
    if response is None:
        logger.error(
            "api_unhandled_exception type=%s request_id=%s",
            type(exc).__name__,
            request_id,
        )
        from .responses import failure

        return failure(
            "internal_error",
            "An unexpected error occurred.",
            status=500,
            request=request,
        )
    detail = response.data
    response.data = {
        "success": False,
        "error": {
            "code": "request_error",
            "message": "Request could not be processed.",
            "details": detail if isinstance(detail, dict) else {"detail": detail},
        },
        "meta": {"request_id": request_id},
    }
    return response
