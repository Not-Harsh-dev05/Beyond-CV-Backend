"""Mocked upstream adapter, retry, certificate, and SSRF tests."""

import socket
import httpx
import pytest
import respx
from django.test import override_settings
from apps.ingestion.security import UnsafeURLError, safe_fetch, validate_public_url
from apps.ingestion.clients.github_client import GitHubClient
from apps.ingestion.clients.kaggle_client import KaggleClient
from apps.ingestion.clients.certificate_client import CertificateClient


def dns_result(ip):
    return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", (ip, 443))]


@override_settings(VERIFICATION_ALLOWED_DOMAINS=["coursera.org", "nptel.ac.in"])
def test_ssrf_rejects_non_allowlisted_and_private_resolution(monkeypatch):
    with pytest.raises(UnsafeURLError):
        validate_public_url("https://evil.example/certificate")
    monkeypatch.setattr(
        socket, "getaddrinfo", lambda *args, **kwargs: dns_result("127.0.0.1")
    )
    with pytest.raises(UnsafeURLError):
        validate_public_url("https://coursera.org/cert/123")
    with pytest.raises(UnsafeURLError):
        validate_public_url("http://coursera.org/cert/123")


@override_settings(VERIFICATION_ALLOWED_DOMAINS=["coursera.org", "nptel.ac.in"])
@respx.mock
def test_redirect_to_internal_ip_is_rejected(monkeypatch):
    monkeypatch.setattr(
        socket,
        "getaddrinfo",
        lambda host, *args, **kwargs: dns_result(
            "8.8.8.8" if host == "coursera.org" else "169.254.1.5"
        ),
    )
    respx.get("https://coursera.org/start").mock(
        return_value=httpx.Response(
            302, headers={"location": "https://nptel.ac.in/internal"}
        )
    )
    with pytest.raises(UnsafeURLError):
        safe_fetch("https://coursera.org/start")


def test_github_retries_server_errors_and_timeout():
    calls, sleeps = {"count": 0}, []

    def handler(request):
        calls["count"] += 1
        if calls["count"] == 1:
            return httpx.Response(503)
        return httpx.Response(200, json={"ok": True})

    client = GitHubClient(
        token="not-a-real-token",
        transport=httpx.MockTransport(handler),
        sleep=sleeps.append,
    )
    assert client._get("/users/sample").json() == {"ok": True}
    assert calls["count"] == 2 and len(sleeps) == 1
    timeout_calls = {"count": 0}

    def timeout_handler(request):
        timeout_calls["count"] += 1
        if timeout_calls["count"] < 3:
            raise httpx.ReadTimeout("simulated timeout")
        return httpx.Response(200, json={"ok": True})

    client = GitHubClient(
        transport=httpx.MockTransport(timeout_handler), sleep=lambda _: None
    )
    assert client._get("/users/sample").status_code == 200
    assert timeout_calls["count"] == 3


def test_github_reads_rate_limit_headers_and_retries():
    calls, slept = {"count": 0}, []

    def handler(request):
        calls["count"] += 1
        if calls["count"] == 1:
            return httpx.Response(
                403, headers={"X-RateLimit-Remaining": "0", "X-RateLimit-Reset": "0"}
            )
        return httpx.Response(200, json=[])

    client = GitHubClient(transport=httpx.MockTransport(handler), sleep=slept.append)
    assert client._get("/users/sample").json() == []
    assert calls["count"] == 2
    assert slept == [0]


def test_github_fetch_verifies_ownership_from_public_gist_content():
    def handler(request):
        if request.url.path == "/users/sample-user":
            return httpx.Response(200, json={"bio": "", "public_repos": 0})
        if request.url.path == "/users/sample-user/repos":
            return httpx.Response(200, json=[])
        if request.url.path == "/users/sample-user/gists":
            return httpx.Response(200, json=[{"id": "gist-1", "description": ""}])
        if request.url.path == "/gists/gist-1":
            return httpx.Response(
                200, json={"files": {"proof.txt": {"content": "verify-BeyondCV-123"}}}
            )
        return httpx.Response(404)

    result = GitHubClient(
        transport=httpx.MockTransport(handler), sleep=lambda _: None
    ).fetch("sample-user", "verify-BeyondCV-123")
    assert result["ownership_verified"] is True
    assert result["method"] == "api"
    assert result["repositories"] == []


@override_settings(KAGGLE_USERNAME="demo", KAGGLE_KEY="fake")
@respx.mock
def test_kaggle_uses_official_api_with_explicit_competition_team():
    route = respx.get(
        "https://www.kaggle.com/api/v1/competitions/house-prices/leaderboard/view"
    ).mock(
        return_value=httpx.Response(200, json={"submissions": [{"teamName": "team-a"}]})
    )
    result = KaggleClient().fetch("house-prices:team-a")
    assert route.called
    assert result["username"] == "team-a"
    assert result["method"] == "api"
    with pytest.raises(RuntimeError):
        KaggleClient().fetch("profile-only")


def test_malformed_certificate_pages_are_unverifiable(monkeypatch):
    monkeypatch.setattr(
        "apps.ingestion.clients.certificate_client.safe_fetch",
        lambda *_args, **_kwargs: (
            "<html><div>javascript required</div></html>",
            "https://coursera.org/x",
        ),
    )
    result = CertificateClient().verify("https://coursera.org/x")
    assert result["status"] == "unverifiable"
    assert result["method"] == "scraped"
    monkeypatch.setattr(
        "apps.ingestion.clients.certificate_client.safe_fetch",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(httpx.ReadTimeout("timeout")),
    )
    failed = CertificateClient().verify("https://coursera.org/x")
    assert failed["status"] == "unverifiable"
    assert "could not be fetched" in failed["reason"]
