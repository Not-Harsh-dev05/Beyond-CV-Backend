"""Envelope and request metadata integration tests."""

import pytest
from types import SimpleNamespace
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_health_envelope_and_request_instance_headers(monkeypatch):
    import redis
    from celery.app.control import Control

    monkeypatch.setattr(
        redis, "from_url", lambda *args, **kwargs: SimpleNamespace(ping=lambda: True)
    )

    class WorkerInspector:
        def ping(self):
            return {"worker@unit-test": {"ok": "pong"}}

    monkeypatch.setattr(Control, "inspect", lambda self, timeout=1: WorkerInspector())
    response = APIClient().get("/api/v1/health/", HTTP_X_REQUEST_ID="trace-test-1")
    assert response.status_code == 200
    assert response.data["success"] is True
    assert response.data["meta"]["request_id"] == "trace-test-1"
    assert response["X-Served-By"]
    assert response["X-Request-ID"] == "trace-test-1"


@pytest.mark.django_db
def test_validation_error_uses_error_envelope():
    response = APIClient().post("/api/v1/auth/register/", {"email": "bad"})
    assert response.status_code == 400
    assert response.data["success"] is False
    assert response.data["error"]["code"] == "request_error"
    assert "request_id" in response.data["meta"]
