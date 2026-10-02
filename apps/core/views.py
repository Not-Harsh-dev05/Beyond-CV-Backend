"""Liveness and dependency health endpoint."""

from django.conf import settings
from django.db import connection
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .responses import success


@api_view(["GET"])
@permission_classes([AllowAny])
def health(request):
    """Report database, Redis, and active Celery worker connectivity."""
    checks = {"database": False, "redis": False, "celery_worker": False}
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        checks["database"] = True
    except Exception:
        pass
    try:
        import redis

        checks["redis"] = bool(
            redis.from_url(settings.CELERY_BROKER_URL, socket_connect_timeout=1).ping()
        )
    except Exception:
        pass
    try:
        from celery import current_app

        inspector = current_app.control.inspect(timeout=1)
        checks["celery_worker"] = bool(inspector and inspector.ping())
    except Exception:
        pass
    status = 200 if all(checks.values()) else 503
    return success(
        {"status": "ok" if status == 200 else "degraded", "checks": checks},
        status=status,
        request=request,
    )
