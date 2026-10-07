# Phase 0 repository audit

Audited on 2026-10-07. The repository contains an existing Django application;
this phase preserves its implementation and records the differences from the
BeyondCV standing requirements. Existing migrations were not changed.

## Complete

- Django 5 project with split base, development, production, and test settings;
  PostgreSQL URL configuration and SQLite development/test settings.
- Custom email-based account model, candidate-only public registration, JWT
  login/refresh/logout, role permissions, throttling, and request metadata.
- Versioned API routes, OpenAPI schema and Swagger UI, pagination, response
  envelopes, and a health endpoint at `/api/v1/health/`.
- Existing profile/evidence, ingestion job/snapshot, job-role, and persisted
  score models, each with initial migrations.
- Celery worker and beat configuration; ingestion creates/reuses active jobs,
  caches source snapshots, and persists score provenance.
- GitHub API client with bounded retry/rate-limit handling and profile-bio or
  public-gist ownership checks. Kaggle API and guarded static certificate-page
  clients also exist.
- Tests cover auth, permissions, API envelopes, ingestion, source handling,
  scoring isolation, ranking, and insights.
- Dockerfile, Compose definitions, pinned Python dependencies, and an
  `.env.example` are present. The example now includes every environment
  variable referenced by settings or Compose.

## Partial

- The existing workflow supports candidate/recruiter/admin roles and a single
  `consent_given` flag. It does not provide the requested STUDENT/HR roles or
  separate `visible_to_hr` and `show_on_leaderboard` controls.
- Candidate profiles, evidence submission, ingestion, explanation-bearing
  scores, role creation, per-role rankings, and aggregate insights exist, but
  the dedicated HR candidate search/detail flow and consent-filtered
  leaderboard are not implemented.
- GitHub evidence can be ownership-checked at ingestion. Kaggle ownership is
  not verified. Certificate URLs use guarded HTML parsing, not a supported
  issuer API. External evidence does not consistently follow the requested
  `source_url`, `fetched_at`, and `verification_level` record contract.
- Existing scoring separates a heuristic evidence competence score from a
  Ridge pedigree baseline, with provenance in a JSON breakdown. It is not the
  requested versioned `baseline-v1` component formula or a normalized
  `ScoreBreakdown` evidence-ID model.
- The configured Compose stack includes PostgreSQL, Redis, web, Celery worker,
  Celery beat, migrations, and Nginx. It could not be started or validated here
  because Docker is not installed; the documented `.env` copy step is needed
  before Compose can load its env file.
- The health endpoint reports dependency checks and returns 503 when any
  dependency is unavailable. Its dependency exceptions are suppressed without
  logging, so diagnosis is limited.
- API errors include the requested `error` object, but are additionally wrapped
  in the application's `success: false` and `meta` envelope.

## Missing

- Explicit `profiles`, `platforms`, `evidence`, `skills`, `roles`,
  `ml_interface`, `hr`, `leaderboard`, and `market` domain apps; existing
  responsibilities instead reside in `candidates`, `ingestion`, `ranking`, and
  `insights`.
- Official Codeforces integration and ownership verification.
- LeetCode and NPTEL provider interfaces with default `UNAVAILABLE` status and
  self-reported evidence support as specified.
- An external JobProvider adapter and the honest disabled-provider response.
- `FeatureBundle`, `PredictionResult`, `MLPredictor`, and the `none`/`http`
  adapter contract; baseline and ML predictions are not independently modeled
  to that contract.
- The requested student-owned profile lifecycle that removes all associated
  derived evidence, independent HR visibility/leaderboard opt-ins, and an
  opted-in leaderboard endpoint.
- A supported source-policy contract for all requested platforms and
  verification levels.

## Broken

- When no trained pedigree artifact exists, scoring automatically trains and
  uses the committed synthetic CSV. The fallback is clearly warned and tagged,
  but it still puts synthetic training data in the application scoring path,
  contrary to the standing no-synthetic-data rule.
- The `seed_demo_data` management command is shipped with the app and creates
  synthetic profiles/scores using hard-coded demo account credentials. It is
  not run automatically and marks the records as sample data, but remains
  unsafe to expose as a production operation under the no-sample-data rule.

## Verification performed

| Command | Result |
|---|---|
| `python -m pytest` | Passed: 45 tests, 15 warnings, 25.34 seconds |
| `python manage.py check` | Passed: no issues (0 silenced); emitted the existing missing-model/synthetic-fallback warning |
| `python manage.py makemigrations --check --dry-run` | Passed: no changes detected |
| `ruff check .` | Passed: all checks passed |
| `docker compose ps` | Not run: `docker` executable is unavailable |

The health test patches Redis and the Celery inspector and asserts HTTP 200 for
`GET /api/v1/health/`. No live web server or external dependency stack was
started, so this does not establish live Compose readiness.
