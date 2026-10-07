# BeyondCV Backend: Standing Instructions

## Environment

This repository is a Django backend. Run commands, tests, and git from the
repository root. Do not claim a command succeeded unless it was run and passed;
report actual output, including failures.

## Product

BeyondCV is a pedigree-blind, evidence-based talent intelligence platform.
Its flow is **EVIDENCE → ANALYSIS → INSIGHT**. Every score must be traceable to
evidence. Users are STUDENT and HR. The backend owns authentication,
authorization, data acquisition, normalization, persistence, APIs, and the
boundary to a separately built ML module.

## Stack

- Python 3.11+, Django 5, Django REST Framework, SimpleJWT
- PostgreSQL (SQLite only for local tests)
- Celery + Redis
- drf-spectacular (OpenAPI), pytest-django
- Docker Compose
- Configuration through environment variables, with a committed `.env.example`

## Hard rules

1. Inspect before changing. Audit existing code first and keep what works. Do
   not rewrite working code. If the repository is empty, scaffold it.
2. No fake, mock, or sample data in application flow or fixtures that ship to
   production. Test doubles are allowed only inside tests.
3. Do not build the ML model. Build only the specified contract and adapter.
4. Never commit secrets. Use environment variables.
5. Never bypass authentication, CAPTCHA, rate limits, or robots.txt. Use
   official APIs where they exist.
6. Architecture: View → Serializer → Service → Model / External API. Keep
   business logic out of views. Put permission logic in reusable permission
   classes.
7. External calls require timeouts, retries with backoff, rate-limit handling,
   and graceful failure that does not crash an API response.
8. Sync tasks must be idempotent: upsert on unique constraints and never
   duplicate rows.
9. All endpoints live under `/api/v1/`. Paginate lists. Use the consistent
   error shape `{"error": {"code": "...", "message": "...", "details": {}}}`.
10. Never edit or delete existing migrations. Add new migrations.
11. Enforce authorization in the backend: 401 unauthenticated, 403 forbidden,
    and 404 for resources the user must not know exist.

## Existing-codebase rules

- Read `docs/AUDIT.md` first. Map every requirement onto the existing apps
  (`accounts`, `candidates`, `ingestion`, `scoring`, `ranking`, `jobs`,
  `insights`, `core`). Do not create parallel apps or duplicate models. Extend
  what exists.
- The existing 45 tests must keep passing. Update a test only if behavior was
  deliberately changed, and say so in the summary.
- Synthetic/demo scoring fallbacks and `seed_demo_data` violate the no-fake-data
  rule; remove or quarantine them in Phase 1B, not before.
- At the start of the next session, ask: “List the rules you loaded from
  AGENTS.md.”

## Data source decision policy

Use a source only if it is an official API or legitimately public data.

- **GitHub:** official REST/GraphQL API with a token from `GITHUB_TOKEN`.
- **Codeforces:** official public API (`codeforces.com/api`).
- **LeetCode:** no official public API. Do not scrape or bypass anything.
  Define a `LeetCodeProvider` interface and implement it only with a documented,
  publicly accessible endpoint if one is allowed; otherwise return
  `status=UNAVAILABLE` and report “source unavailable”. Also support
  student-submitted evidence (profile URL plus ownership verification), clearly
  labelled `self_reported`.
- **NPTEL:** no public API. Use the same unavailable-by-default pattern with a
  `NptelProvider` interface, plus student-submitted certificate records
  (course, score, certificate URL/ID) labelled `self_reported` until verified.
- **Jobs:** define a `JobProvider` interface. Implement one real provider only
  if its API key is present in the environment (for example, Adzuna or a
  similar free-tier API). Without a configured key, disable the provider and
  return empty results with a “no provider configured” message. Never invent
  jobs.

Every evidence row carries `source`, `source_url`, `fetched_at`, and
`verification_level` (`VERIFIED` | `SELF_REPORTED` | `UNAVAILABLE`).

## Ownership verification

Students must prove ownership of an external profile before it counts as
`VERIFIED`.

- **GitHub:** GitHub OAuth, or a verification token placed in the profile bio
  or a public gist.
- **Codeforces:** temporarily place a token in a profile field (for example,
  organization).
- **LeetCode / NPTEL:** place a token in public profile text if technically
  possible; otherwise keep evidence `SELF_REPORTED`.

The backend generates a random, single-use token, checks it through the
provider, and then marks the `ExternalProfile` `VERIFIED`. Unverified evidence
is shown but weighted lower.

## Consent and privacy

`StudentProfile` has `visible_to_hr` (default `False`) and
`show_on_leaderboard` (default `False`). HR endpoints and the leaderboard only
include students who opted in. Students can delete external profiles and all
derived evidence. Leaderboard and compare responses must not contain private
data such as email or phone.

## Baseline scoring

Until the ML module is connected, compute a deterministic, transparent,
versioned `baseline-v1` formula in `scoring/baseline.py`. Normalize each
component to 0–100 using documented caps:

- **GitHub (30%):** repositories, stars, forks, language diversity, recent
  activity.
- **Coding (30%):** Codeforces rating and solved count; LeetCode solved count
  and difficulty mix.
- **Certifications (15%):** NPTEL/other certificate count and scores.
- **Projects (15%):** project count, stars, and evidence links.
- **Skills breadth (10%):** number of skills above the score threshold.

Overall is the weighted sum over available components, with weights
renormalized. Verification multiplier: `VERIFIED` 1.0,
`SELF_REPORTED` 0.6. A missing component is `null`, never 0. Store a
`ScoreBreakdown` (component, raw inputs, normalized value, weight, evidence
IDs) so every score can be explained. Store ML output separately; it must
never overwrite the baseline.

## ML contract (interface only)

Define in `ml_interface/contract.py`:

- `FeatureBundle` (dataclass or Pydantic): `contract_version="1.0"`,
  `student_id`, `skill_vector` (`{skill_slug: 0-1}`), `platform_metrics`
  (`github`, `leetcode`, `codeforces`, `nptel`), `project_metrics`,
  `coding_metrics`, `experience`, `education`, `role_requirements`,
  `market_features`, and `generated_at`.
- `PredictionResult`: `contract_version`, `model_version`, `student_id`,
  `competence` (0–100 or `null`), `role_fit`
  (`[{role_slug, score, confidence}]`), `skill_gaps`
  (`[{skill_slug, gap, priority}]`), `recommendations` (strings),
  `future_skill_signals` (`[{skill_slug, trend, confidence}]`), and
  `generated_at`.
- `MLPredictor(Protocol)` with `predict(bundle: FeatureBundle) ->
  PredictionResult` and `predict_batch(bundles) -> list[PredictionResult]`.

Select implementations through `ML_BACKEND = "none" | "http"`. The default
`none` backend returns nulls. The `http` backend POSTs bundle JSON to
`ML_SERVICE_URL` with a 10-second timeout, retries twice, validates the response
against the schema, and on failure returns a null `PredictionResult` and logs
an error; it never raises to the API caller. Single-student predictions are
synchronous with caching; batch/leaderboard refresh runs as a Celery task.
Include `model_version` and `contract_version` in every stored prediction.
Bumping `contract_version` is required for breaking changes.

## Demo-critical path

Finish this path first:

Register → login → student opts in → connects GitHub + Codeforces → ownership
verified → background sync → baseline score with breakdown → HR logs in →
searches/filters candidates → opens candidate with evidence and “why” →
leaderboard.

Everything else (jobs, market, trends, NPTEL, LeetCode) is secondary and may
ship as a clean interface with an honest “unavailable” state.

## Phase workflow

At the start of each phase: read this file, run `git status`, and run the test
suite.

At the end of each phase: run migration checks, tests, and Ruff; update README
for what actually works; commit with a conventional message; then report:

1. What was already there and what was added/changed (files).
2. Models/migrations.
3. Endpoints added.
4. Commands run and their real output, including test passed/failed counts.
5. Acceptance criteria, each marked PASS/FAIL with proof.
6. Known limitations / things not done.
7. Git commit hash.

## Phase 0: audit and foundation

Read this file. If the repository already contains code, inspect it and audit
it before changing anything. Produce `docs/AUDIT.md` with four lists:
Complete / Partial / Missing / Broken. Do not change working code except to fix
what blocks running it.

If the repository is empty, scaffold a Django project called `config`, with
apps split into `accounts`, `profiles`, `platforms`, `evidence`, `skills`,
`roles`, `scoring`, `ml_interface`, `hr`, `leaderboard`, `jobs`, and `market`;
settings split into base/dev/prod; Docker Compose (web, PostgreSQL, Redis,
Celery worker); requirements; `.env.example`; pytest and Ruff configuration;
drf-spectacular at `/api/v1/docs/`; `GET /api/v1/health/`; and the standard
error handler.

Phase 0 acceptance criteria:

- `python manage.py check` passes with no errors.
- `python manage.py makemigrations --check` reports no pending changes.
- `docker compose up` starts web, database, Redis, and worker (or document why
  Docker is unavailable).
- `GET /api/v1/health/` returns 200.
- pytest runs and passes, even if only a health test exists.
- `docs/AUDIT.md` exists and is accurate.
- `.env.example` lists every environment variable used; no secrets are
  committed.
