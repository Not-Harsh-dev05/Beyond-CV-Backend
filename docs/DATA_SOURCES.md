# Data sources and limitations

| Source | Acquisition | Verification and limits | Failure behavior |
|---|---|---|---|
| GitHub | GitHub REST API v3 (`api.github.com`) using public endpoints; optional `GITHUB_TOKEN`; paginated repositories (currently capped at 500 per fetch); README retrieval is capped at the 25 most recently updated repositories. | Ownership is checked by finding the candidate's one-time code in public profile bio or public gist description/content. This proves control of the account/gist at fetch time, not authorship of every repository. Repository source code is not fetched; project substance uses repository metadata and README text. Respect GitHub API rate limits and terms; `X-RateLimit-Remaining` and `X-RateLimit-Reset` are inspected. | Retries 429/5xx/timeouts with bounded backoff and jitter, handles primary rate limit reset, and surfaces failed source metadata. |
| Kaggle | Official Kaggle API leaderboard endpoint with `KAGGLE_USERNAME`/`KAGGLE_KEY`; candidate must supply `competition-slug:team-name`. Profile-wide result discovery by username is not implemented because there is no supported stable public endpoint for it. | This is an API method, not profile-page scraping. A leaderboard row is not strong identity proof that the candidate controls a Kaggle account; Kaggle ownership verification is not implemented. API response shapes and access requirements may vary with Kaggle's service. | Missing credentials, unsupported handle, unavailable competition, or unexpected payload is reported as a failed/unavailable source. No metric is invented. |
| NPTEL/Coursera certificates | Candidate-supplied verification URL fetched with `httpx` and parsed with BeautifulSoup. HTML method is explicitly labeled `scraped` in snapshots/signals. | HTTPS and allowlisted hosts are required; DNS answers must be globally routable; redirects are revalidated; response is capped at 2 MB and timeout is 10 seconds. Static pages only. Dynamic pages, login walls, altered markup, and weak issuer evidence return `unverifiable`. Text heuristics are not cryptographic issuer verification. | Safe fetch/parse errors become an explicit structured `unverifiable` result; candidate evidence source is recorded as failed if a request-level fetch itself fails. |

Unverified GitHub/Kaggle evidence is still eligible for scoring with reduced weight. Certificate scoring is nonzero only when a static page explicitly describes a credential as verified/valid. The system never substitutes a fake source response for a real fetch.

## Partial functionality

- GitHub only retrieves repository metadata plus README text for up to 25 recent repositories; it does not inspect code contents or use a validated originality model. Challenge code confirms control of a GitHub account/gist, not ownership of each project.
- Kaggle team-name matching and leaderboard rank are not a reliable identity check; account ownership is unavailable.
- Certificate text matching is heuristic, cannot prove issuer authenticity, and dynamic verification flows remain unsupported.
- Competence and role fit scales are initial transparent heuristics; the included pedigree baseline fallback uses synthetic rows. Production hiring decisions require validated, representative, lawfully obtained training/evaluation data and model governance.
- Skill insights use language names as a proxy for skills. No candidate-level insight is returned, but k-suppression is not a complete re-identification defense against external auxiliary data.

For every upstream source, confirm current terms, API policies, and credentials in the deployment jurisdiction before enabling production collection. Source adapters intentionally make no guarantee of completeness.
