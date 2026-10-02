"""GitHub REST API client with bounded retry and pagination behavior."""

import base64
import random
import time
from urllib.parse import quote
import httpx
from django.conf import settings

API = "https://api.github.com"


class GitHubClient:
    """Fetch user, repositories, and ownership verification evidence."""

    def __init__(self, *, token=None, transport=None, sleep=time.sleep):
        self.token = settings.GITHUB_TOKEN if token is None else token
        self.transport = transport
        self.sleep = sleep

    def _get(self, path, params=None):
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        with httpx.Client(
            timeout=httpx.Timeout(10), transport=self.transport
        ) as client:
            for attempt in range(4):
                try:
                    response = client.get(
                        f"{API}{path}", params=params, headers=headers
                    )
                except httpx.TimeoutException:
                    if attempt == 3:
                        raise
                    self.sleep(min(8, 0.5 * (2**attempt)) + random.uniform(0, 0.25))
                    continue
                remaining = int(response.headers.get("X-RateLimit-Remaining", "1"))
                if response.status_code == 403 and remaining == 0:
                    reset = int(response.headers.get("X-RateLimit-Reset", "0"))
                    self.sleep(max(0, min(reset - int(time.time()), 60)))
                    continue
                if response.status_code == 429 or response.status_code >= 500:
                    if attempt == 3:
                        response.raise_for_status()
                    retry_after = float(response.headers.get("Retry-After", 0))
                    self.sleep(
                        retry_after
                        or min(8, 0.5 * (2**attempt)) + random.uniform(0, 0.25)
                    )
                    continue
                response.raise_for_status()
                return response
        raise httpx.HTTPError("GitHub API retry limit exceeded.")

    def fetch(self, username: str, verification_code: str = "") -> dict:
        """Collect live public GitHub account and up to 500 repository summaries."""
        user = self._get(f"/users/{username}").json()
        repos = []
        for page in range(1, 6):
            batch = self._get(
                f"/users/{username}/repos",
                {"per_page": 100, "page": page, "sort": "updated"},
            ).json()
            if not batch:
                break
            repos.extend(batch)
            if len(batch) < 100:
                break
        project_rows = sorted(
            repos, key=lambda repo: repo.get("updated_at") or "", reverse=True
        )
        for repo in project_rows[:25]:
            full_name = repo.get("full_name") or f"{username}/{repo.get('name', '')}"
            try:
                readme = self._get(f"/repos/{quote(full_name, safe='/')}/readme").json()
                repo["readme"] = base64.b64decode(readme.get("content", "")).decode(
                    "utf-8", errors="replace"
                )[:12000]
            except (httpx.HTTPError, ValueError):
                repo["readme"] = ""
        ownership = bool(
            verification_code and verification_code in (user.get("bio") or "")
        )
        if verification_code and not ownership:
            try:
                gists = self._get(f"/users/{username}/gists", {"per_page": 100}).json()
                for gist in gists:
                    if verification_code in str(gist.get("description", "")):
                        ownership = True
                        break
                    details = self._get(f"/gists/{gist['id']}").json()
                    if any(
                        verification_code in str(file.get("content", ""))
                        for file in details.get("files", {}).values()
                    ):
                        ownership = True
                        break
            except httpx.HTTPError:
                ownership = False
        return {
            "user": {
                "public_repos": user.get("public_repos", 0),
                "followers": user.get("followers", 0),
                "created_at": user.get("created_at"),
                "bio": user.get("bio", ""),
            },
            "repositories": [
                {
                    "name": r.get("name", ""),
                    "description": r.get("description", ""),
                    "stars": r.get("stargazers_count", 0),
                    "forks": r.get("forks_count", 0),
                    "size": r.get("size", 0),
                    "fork": r.get("fork", False),
                    "readme": r.get("readme", ""),
                    "updated_at": r.get("updated_at"),
                    "language": r.get("language"),
                }
                for r in repos
            ],
            "ownership_verified": ownership,
            "method": "api",
        }
