"""Safe parser for static NPTEL and Coursera certificate verification pages."""

import re
from bs4 import BeautifulSoup
import httpx
from apps.ingestion.security import safe_fetch, UnsafeURLError


class CertificateClient:
    """Return structured verification outcomes without propagating page parsing errors."""

    def verify(self, url: str) -> dict:
        """Fetch an allowlisted verification page and extract available public fields."""
        try:
            html, final_url = safe_fetch(url, timeout=10)
            soup = BeautifulSoup(html, "html.parser")
            text = " ".join(soup.stripped_strings)
            if not text or len(text) < 10:
                return {
                    "status": "unverifiable",
                    "reason": "Verification page contained no readable certificate details.",
                    "method": "scraped",
                }
            verified = re.search(
                r"\b(credential|certificate)\s+(is\s+)?(valid|verified)\b|\bsuccessfully verified\b",
                text,
                re.I,
            )
            return {
                "status": "verified" if verified else "unverifiable",
                "title": soup.title.get_text(" ", strip=True) if soup.title else "",
                "text_excerpt": text[:1000],
                "url": final_url,
                "method": "scraped",
            }
        except UnsafeURLError:
            return {
                "status": "unverifiable",
                "reason": "Verification URL failed safety checks.",
                "method": "scraped",
            }
        except (httpx.HTTPError, OSError, UnicodeError, ValueError):
            return {
                "status": "unverifiable",
                "reason": "Verification page could not be fetched or parsed.",
                "method": "scraped",
            }
