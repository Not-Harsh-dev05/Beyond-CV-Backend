"""Kaggle's official competition API client; it never scrapes profile pages."""

import httpx
from django.conf import settings


class KaggleClient:
    """Retrieve public competition leaderboard data using Kaggle credentials."""

    base_url = "https://www.kaggle.com/api/v1"

    def fetch_leaderboard(self, competition: str) -> dict:
        """Fetch leaderboard rows; Kaggle credential/API failures stay explicit."""
        if not settings.KAGGLE_USERNAME or not settings.KAGGLE_KEY:
            raise RuntimeError("Kaggle API credentials are not configured.")
        with httpx.Client(
            timeout=httpx.Timeout(10),
            auth=(settings.KAGGLE_USERNAME, settings.KAGGLE_KEY),
        ) as client:
            response = client.get(
                f"{self.base_url}/competitions/{competition}/leaderboard/view",
                params={"page": 1, "pageSize": 100},
            )
            response.raise_for_status()
            return {
                "leaderboard": response.json(),
                "competition": competition,
                "method": "api",
            }

    def fetch(self, reference: str) -> dict:
        """Fetch a leaderboard for a supplied competition:team reference."""
        if ":" not in reference:
            raise RuntimeError(
                "Provide a Kaggle evidence handle as competition-slug:team-name."
            )
        competition, username = reference.split(":", 1)
        result = self.fetch_leaderboard(competition)
        payload = result["leaderboard"]
        rows = (
            payload
            if isinstance(payload, list)
            else payload.get("submissions", payload.get("leaderboard", []))
        )
        if not isinstance(rows, list):
            raise RuntimeError("Kaggle API returned an unsupported leaderboard format.")
        return {
            "leaderboard": rows,
            "competition": competition,
            "username": username,
            "method": "api",
        }
