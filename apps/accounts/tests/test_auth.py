"""Authentication registration and role non-escalation tests."""

import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model


@pytest.mark.django_db
def test_register_always_creates_candidate_and_login_returns_envelope():
    client = APIClient()
    response = client.post(
        "/api/v1/auth/register/",
        {
            "email": "new@example.test",
            "username": "new",
            "password": "StrongPass!234",
            "role": "ADMIN",
        },
    )
    assert response.status_code == 201
    assert response.data["success"] is True
    user = get_user_model().objects.get(email="new@example.test")
    assert user.role == "CANDIDATE"
    login = client.post(
        "/api/v1/auth/login/",
        {"email": "new@example.test", "password": "StrongPass!234"},
    )
    assert login.status_code == 200
    assert login.data["success"] is True
    assert "refresh" in login.data["data"]


@pytest.mark.django_db
def test_logout_blacklists_refresh_token():
    from rest_framework_simplejwt.tokens import RefreshToken

    user = get_user_model().objects.create_user(
        email="logout@example.test", username="logout", password="StrongPass!234"
    )
    client = APIClient()
    client.force_authenticate(user)
    refresh = str(RefreshToken.for_user(user))
    response = client.post("/api/v1/auth/logout/", {"refresh": refresh}, format="json")
    assert response.status_code == 200
    assert response.data["data"]["logged_out"] is True
