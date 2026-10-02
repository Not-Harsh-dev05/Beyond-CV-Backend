"""SSRF-resistant validation and bounded fetching for candidate URLs."""

import ipaddress
import socket
from urllib.parse import urljoin, urlparse
import httpx
from django.conf import settings

MAX_RESPONSE_BYTES = 2_000_000
MAX_REDIRECTS = 3


class UnsafeURLError(ValueError):
    """Raised when a URL violates SSRF protection policy."""


def validate_public_url(url: str) -> str:
    """Require HTTPS, allowlisted host and exclusively public DNS answers."""
    parsed = urlparse(url)
    if (
        parsed.scheme != "https"
        or not parsed.hostname
        or parsed.username
        or parsed.password
    ):
        raise UnsafeURLError("Only credential-free HTTPS URLs are permitted.")
    host = parsed.hostname.rstrip(".").lower()
    allowed = [
        d.strip().lower().lstrip(".") for d in settings.VERIFICATION_ALLOWED_DOMAINS
    ]
    if not any(host == domain or host.endswith("." + domain) for domain in allowed):
        raise UnsafeURLError("URL host is not allowlisted.")
    try:
        addresses = {
            item[4][0]
            for item in socket.getaddrinfo(
                host, parsed.port or 443, type=socket.SOCK_STREAM
            )
        }
    except OSError as exc:
        raise UnsafeURLError("URL host could not be resolved.") from exc
    if not addresses:
        raise UnsafeURLError("URL host did not resolve.")
    for address in addresses:
        ip = ipaddress.ip_address(address.split("%")[0])
        if not ip.is_global:
            raise UnsafeURLError("URL resolves to a non-public address.")
    return url


def safe_fetch(url: str, *, timeout: float = 10.0) -> tuple[str, str]:
    """Fetch bounded HTML while validating each redirect hop."""
    current = validate_public_url(url)
    limits = httpx.Limits(max_connections=2, max_keepalive_connections=0)
    with httpx.Client(
        timeout=httpx.Timeout(timeout), follow_redirects=False, limits=limits
    ) as client:
        for redirect_count in range(MAX_REDIRECTS + 1):
            with client.stream(
                "GET", current, headers={"User-Agent": "BeyondCV/1.0"}
            ) as response:
                if response.status_code in (301, 302, 303, 307, 308):
                    if redirect_count >= MAX_REDIRECTS:
                        raise UnsafeURLError("Too many redirects.")
                    location = response.headers.get("location")
                    if not location:
                        raise UnsafeURLError("Redirect omitted a destination.")
                    current = validate_public_url(urljoin(current, location))
                    continue
                response.raise_for_status()
                chunks = []
                total = 0
                for chunk in response.iter_bytes():
                    total += len(chunk)
                    if total > MAX_RESPONSE_BYTES:
                        raise UnsafeURLError(
                            "Response exceeds the maximum allowed size."
                        )
                    chunks.append(chunk)
                return b"".join(chunks).decode(
                    response.encoding or "utf-8", errors="replace"
                ), str(response.url)
    raise UnsafeURLError("Unable to fetch URL safely.")
