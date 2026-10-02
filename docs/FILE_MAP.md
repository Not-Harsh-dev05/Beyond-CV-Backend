# Complete file map

Every committed source, migration, test, configuration, and documentation file is listed below; package `__init__.py` files mark Python packages.

| Path | Responsibility |
|---|---|
| `.dockerignore` | Excludes secrets, local databases, model artifacts, and generated files from Docker build context |
| `.env.example` | Local Compose environment template |
| `.gitignore` | Excludes secrets, generated databases, coverage output, and model artifacts from version control |
| `Dockerfile` | Python 3.12 CPU-only application image and build-time embedding model download |
| `Makefile` | Build, run, migration, test, lint, model, seed, and log shortcuts |
| `README.md` | Quickstart, overview, and operator entry points |
| `docker-compose.yml` | PostgreSQL, Redis, migration runner, web replicas, Celery, and Nginx services |
| `manage.py` | Django management command entry point |
| `pytest.ini` | Django test settings and 80% coverage threshold |
| `requirements/base.txt` | Pinned runtime dependencies, including CPU PyTorch |
| `requirements/dev.txt` | Pinned test and development tools |
| `requirements/prod.txt` | Production dependency set |
| `nginx/nginx.conf` | Docker-DNS-aware reverse proxy, static asset service, retries, gzip, and headers |
| `config/__init__.py` | Exposes the Celery application |
| `config/asgi.py` | ASGI entry point |
| `config/celery.py` | Celery application and task discovery |
| `config/urls.py` | API v1, authentication, health, schema, and Swagger routing |
| `config/wsgi.py` | Gunicorn WSGI entry point |
| `config/settings/__init__.py` | Settings package marker |
| `config/settings/base.py` | Shared app, DB, security, API, source, ranking, and Celery settings |
| `config/settings/dev.py` | SQLite development settings |
| `config/settings/prod.py` | Production secret, database, host, cookie, and HTTPS settings |
| `config/settings/test.py` | In-memory SQLite, eager Celery, and deterministic test settings |
| `apps/__init__.py` | Applications package marker |
| `apps/core/__init__.py` | Core package marker |
| `apps/core/apps.py` | Core Django application configuration |
| `apps/core/cors.py` | Origin allowlist CORS middleware |
| `apps/core/exceptions.py` | DRF exception envelope and opaque server errors |
| `apps/core/middleware.py` | Request ID and `X-Served-By` response metadata |
| `apps/core/pagination.py` | Shared API pagination envelope and source/sample metadata |
| `apps/core/responses.py` | Standard success and error response builders |
| `apps/core/throttling.py` | Role-based and anonymous request throttling |
| `apps/core/utils.py` | Stable SHA-256 identifier utility |
| `apps/core/views.py` | Database, Redis, and Celery worker readiness endpoint |
| `apps/core/management/__init__.py` | Core management package marker |
| `apps/core/management/commands/__init__.py` | Core management command package marker |
| `apps/core/management/commands/seed_demo_data.py` | Explicit idempotent synthetic sample-data seeder |
| `apps/core/migrations/__init__.py` | Core migrations package marker |
| `apps/core/migrations/0001_initial.py` | Core initial migration marker |
| `apps/core/tests/__init__.py` | Core tests package marker |
| `apps/core/tests/test_api_core.py` | API envelope, health, request ID, and instance header tests |
| `apps/accounts/__init__.py` | Accounts package marker |
| `apps/accounts/admin.py` | Django admin registration for the custom user |
| `apps/accounts/apps.py` | Accounts Django application configuration |
| `apps/accounts/models.py` | Custom user, application roles, and admin-aware user manager |
| `apps/accounts/permissions.py` | Role and candidate-owner permission classes |
| `apps/accounts/serializers.py` | Candidate registration and role-bearing JWT serializers |
| `apps/accounts/urls.py` | Authentication endpoint routes |
| `apps/accounts/views.py` | Registration, login, token refresh, and refresh-token logout |
| `apps/accounts/migrations/__init__.py` | Accounts migrations package marker |
| `apps/accounts/migrations/0001_initial.py` | Custom user schema migration |
| `apps/accounts/tests/__init__.py` | Accounts tests package marker |
| `apps/accounts/tests/test_auth.py` | Registration non-escalation, JWT, and logout tests |
| `apps/candidates/__init__.py` | Candidates package marker |
| `apps/candidates/admin.py` | Django admin registrations for profiles and evidence |
| `apps/candidates/apps.py` | Candidates Django application configuration |
| `apps/candidates/models.py` | Candidate profile and source evidence-link models |
| `apps/candidates/serializers.py` | Profile and candidate-owned evidence serializers |
| `apps/candidates/urls.py` | Candidate self-service, evidence, and score routes |
| `apps/candidates/views.py` | Candidate CRUD, ownership enforcement, account deletion, and score access |
| `apps/candidates/migrations/__init__.py` | Candidates migrations package marker |
| `apps/candidates/migrations/0001_initial.py` | Candidate profile and evidence schema migration |
| `apps/candidates/tests/__init__.py` | Candidates tests package marker |
| `apps/candidates/tests/test_candidate_permissions.py` | Ownership, consent, deletion, and sample-provenance tests |
| `apps/ingestion/__init__.py` | Ingestion package marker |
| `apps/ingestion/admin.py` | Django admin registrations for jobs and snapshots |
| `apps/ingestion/apps.py` | Ingestion Django application configuration |
| `apps/ingestion/models.py` | Idempotent jobs, active-job uniqueness, and TTL signal snapshots |
| `apps/ingestion/security.py` | HTTPS/domain/DNS/redirect/size/timeout SSRF guard |
| `apps/ingestion/services.py` | Source cache, live acquisition, identity redaction, and scoring orchestration |
| `apps/ingestion/tasks.py` | Retryable Celery processing and job state management |
| `apps/ingestion/urls.py` | Ingestion submission and polling routes |
| `apps/ingestion/views.py` | Consent-checked ingestion request and owner-scoped polling |
| `apps/ingestion/clients/__init__.py` | Source client package marker |
| `apps/ingestion/clients/certificate_client.py` | Safe static certificate-page parsing |
| `apps/ingestion/clients/github_client.py` | GitHub REST, pagination, retry, README, and ownership verification |
| `apps/ingestion/clients/kaggle_client.py` | Official Kaggle competition leaderboard API adapter |
| `apps/ingestion/migrations/__init__.py` | Ingestion migrations package marker |
| `apps/ingestion/migrations/0001_initial.py` | Ingestion job and snapshot schema migration |
| `apps/ingestion/tests/__init__.py` | Ingestion tests package marker |
| `apps/ingestion/tests/test_ingestion_service.py` | Deduplication, cache, consent, redaction, and partial-source tests |
| `apps/ingestion/tests/test_sources_and_security.py` | Mocked APIs, retries, malformed certificates, and SSRF tests |
| `apps/ingestion/tests/test_tasks.py` | Celery job completion, failure, and duplicate-delivery tests |
| `apps/scoring/__init__.py` | Scoring package marker |
| `apps/scoring/admin.py` | Score-result Django admin registration |
| `apps/scoring/apps.py` | Scoring Django application configuration |
| `apps/scoring/competence.py` | Strict evidence-only competence scorer and project heuristic |
| `apps/scoring/delta.py` | Pure competence-minus-baseline delta calculation |
| `apps/scoring/embeddings.py` | Lazy local, API, and deterministic embedding backends |
| `apps/scoring/models.py` | Persisted score, provenance, source, and sample-data model |
| `apps/scoring/pedigree.py` | Ridge baseline training, versioned persistence, and explicit fallback |
| `apps/scoring/urls.py` | Pedigree model administration routes |
| `apps/scoring/views.py` | Admin-only baseline retraining API |
| `apps/scoring/data/pedigree_train_SAMPLE_SYNTHETIC.csv` | Clearly labeled synthetic fallback training dataset |
| `apps/scoring/management/__init__.py` | Scoring management package marker |
| `apps/scoring/management/commands/__init__.py` | Scoring command package marker |
| `apps/scoring/management/commands/train_pedigree_model.py` | `train_pedigree_model --data-path` command |
| `apps/scoring/migrations/__init__.py` | Scoring migrations package marker |
| `apps/scoring/migrations/0001_initial.py` | Persisted score schema migration |
| `apps/scoring/normalizers/__init__.py` | Normalizer package marker |
| `apps/scoring/normalizers/certificates.py` | Verified certificate depth normalization |
| `apps/scoring/normalizers/github.py` | GitHub activity and repository substance normalization |
| `apps/scoring/normalizers/kaggle.py` | Kaggle leaderboard percentile normalization |
| `apps/scoring/tests/__init__.py` | Scoring tests package marker |
| `apps/scoring/tests/test_isolation.py` | Confirms profile identity/pedigree changes do not change competence |
| `apps/scoring/tests/test_scoring.py` | Delta, normalizer, scorer, and baseline tests |
| `apps/jobs/__init__.py` | Jobs package marker |
| `apps/jobs/admin.py` | Job-role Django admin registration |
| `apps/jobs/apps.py` | Jobs Django application configuration |
| `apps/jobs/models.py` | Job roles, skill weights, and sample provenance |
| `apps/jobs/serializers.py` | Job-role validation and representation |
| `apps/jobs/urls.py` | Job list and creation routes |
| `apps/jobs/views.py` | Authenticated job listing and recruiter/admin creation |
| `apps/jobs/migrations/__init__.py` | Jobs migrations package marker |
| `apps/jobs/migrations/0001_initial.py` | Job-role schema migration |
| `apps/jobs/tests/__init__.py` | Jobs tests package marker |
| `apps/jobs/tests/test_jobs.py` | Recruiter job-creation permissions |
| `apps/ranking/__init__.py` | Ranking package marker |
| `apps/ranking/apps.py` | Ranking Django application configuration |
| `apps/ranking/services.py` | Consent-filtered role fit, delta, rationale, and sorting |
| `apps/ranking/urls.py` | Recruiter job-ranking routes |
| `apps/ranking/views.py` | Recruiter-only paginated ranking API |
| `apps/ranking/migrations/__init__.py` | Ranking migrations package marker |
| `apps/ranking/migrations/0001_initial.py` | Ranking initial migration marker (ranking is computed) |
| `apps/ranking/tests/__init__.py` | Ranking tests package marker |
| `apps/ranking/tests/test_ranking.py` | Ranking formula, evidence, and consent tests |
| `apps/insights/__init__.py` | Insights package marker |
| `apps/insights/admin.py` | Insights admin module; aggregates are computed, not stored |
| `apps/insights/apps.py` | Insights Django application configuration |
| `apps/insights/services.py` | k-suppressed aggregated skill insights |
| `apps/insights/urls.py` | Undervalued-skill route |
| `apps/insights/views.py` | Admin-only aggregate insights endpoint |
| `apps/insights/migrations/__init__.py` | Insights migrations package marker |
| `apps/insights/migrations/0001_initial.py` | Insights initial migration marker (aggregates are computed) |
| `apps/insights/tests/__init__.py` | Insights tests package marker |
| `apps/insights/tests/test_insights.py` | Aggregate k-threshold and administrator access tests |
| `docs/ARCHITECTURE.md` | Data flow, privacy boundaries, and scoring formulas |
| `docs/API.md` | Endpoint, request, response, and provenance contract |
| `docs/ASSUMPTIONS.md` | Explicit product and implementation assumptions |
| `docs/AUTH.md` | Role matrix, JWT, consent, and permission rules |
| `docs/DATA_SOURCES.md` | Source APIs, verification limits, scraping, and failure behavior |
| `docs/DEPLOYMENT.md` | Compose operation, scaling, and production checklist |
| `docs/FILE_MAP.md` | This per-file responsibility map |
| `docs/TESTING.md` | Mocked test setup, coverage threshold, and commands |
