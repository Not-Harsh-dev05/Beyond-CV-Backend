# API reference

Base URL: `/api/v1/`. Authenticate with `Authorization: Bearer <access-token>`. JSON responses use:

```json
{"success":true,"data":{"id":1},"meta":{"request_id":"...","sources_used":[],"sources_failed":[],"is_sample_data":false}}
```

Errors use `success: false`, an `error` object with `code`, `message`, and `details`, and `meta.request_id`. List routes paginate with `page` and `page_size`.

## Authentication

- `POST /auth/register/`: `{ "email":"candidate@example.test", "username":"candidate", "password":"..." }`. Creates a candidate role only.
- `POST /auth/login/`: `{ "email":"...", "password":"..." }`; returns access and refresh tokens.
- `POST /auth/refresh/`: `{ "refresh":"..." }`; rotates the refresh token.
- `POST /auth/logout/`: authenticated `{ "refresh":"..." }`; blacklists that token.

## Candidate evidence

- `GET|PUT|DELETE /candidates/me/`: profile self-service and account/data erasure. Profile fields include `name`, `gender`, `college_tier`, `employer_brand`, `region`, and `consent_given`.
- `POST /candidates/me/evidence/`: `{ "source":"github", "handle":"octocat" }`; response issues the ownership challenge code. Certificates use `source: "certificate"` and an allowlisted `url`. Kaggle `handle` is `competition-slug:team-name`.
- `PATCH|DELETE /candidates/me/evidence/{id}/`: edit a locator or delete owned evidence; changing a locator invalidates cached snapshots and creates a fresh GitHub challenge code.
- `GET /candidates/{id}/score/`: self or recruiter viewing a consenting candidate; returns competence, baseline, delta, baseline provenance, source breakdown and failures.
- `POST /ingestion/jobs/`: candidate with consent. Returns HTTP 202 and `{ "job_id": 1, "status":"PENDING" }`. Pass `{ "refresh": true }` to bypass cached source snapshots and fetch current upstream data; explicit refreshes are limited to once per `INGESTION_MIN_REFRESH_MINUTES` (10 by default). Ordinary requests reuse snapshots until `SIGNAL_TTL_HOURS` expires.
- `GET /ingestion/jobs/{id}/`: owner/admin polls `PENDING`, `RUNNING`, `SUCCESS`, or `FAILED`.

Example ranking entry:

```json
{"candidate_id":17,"competence":72.0,"baseline":48.0,"delta":24.0,"baseline_source":"sample_synthetic","role_fit":75.0,"normalized_delta":62.0,"ranking_score":71.1,"matched_skills":["python"],"required_skills":["python","django"],"evidence_breakdown":{"github":{"score":72.0,"weight":0.65,"ownership_verified":false}},"sources_used":["github"],"sources_failed":[],"ownership_verified":false,"rationale":"Candidate shows a +24 competence delta over the pedigree baseline, with evidence from github. Matched 1 of 2 required skills.","is_sample_data":false}
```

## Jobs, rankings, insights, administration

- `GET|POST /jobs/`: list roles; recruiters/admins create `{ "title":"Backend Engineer", "required_skills":["Python","Django"], "skill_weights":{"Python":2} }`.
- `GET /jobs/{id}/ranking/`: recruiter/admin; only consenting profiles with scores are ranked.
- `GET /insights/undervalued-skills/?region=...&tier=TIER_3`: admin-only paginated aggregate insights; groups below k are omitted.
- `POST /admin/pedigree-model/train/`: admin only, `{ "data_path":"/mounted/path/train.csv" }`. CSV must contain `college_tier`, `employer_brand`, `competence`; use a trusted server-local path.
- `GET /health/`, `/docs/`, `/schema/`: database/Redis/Celery-worker readiness, Swagger UI, OpenAPI schema.

The sample JSON above is illustrative only. Real API responses are based on persisted live data; only explicit demo-seeder rows have `is_sample_data: true`.
