# BeyondCV backend

BeyondCV is a Django REST backend for evidence-based talent discovery. Candidate-provided public evidence is fetched live, scored independently of pedigree, and compared to a separately trained pedigree baseline. Synthetic data is created only by the explicit demo seeder and is always labeled.

## Start in under five minutes

Requirements: Docker Engine with Compose v2 and a network connection for the initial image/model download.

```sh
cp .env.example .env
# Change SECRET_KEY and POSTGRES_PASSWORD before any shared or production deployment.
docker compose up --build
```

Open [http://localhost/api/v1/docs/](http://localhost/api/v1/docs/) for Swagger and [http://localhost/api/v1/health/](http://localhost/api/v1/health/) for dependency status. The app listens through Nginx on port 80. Set a `GITHUB_TOKEN` for higher API rate limits and Kaggle credentials for supplied competition leaderboards.

For local development, create a Python 3.12 virtual environment, install `requirements/dev.txt`, set `DJANGO_SETTINGS_MODULE=config.settings.dev`, then run `python manage.py migrate` and `python manage.py runserver`.

## API

All API routes are versioned under `/api/v1/`; see [docs/API.md](docs/API.md). Responses use a common envelope and carry `meta.request_id`. Read [docs/AUTH.md](docs/AUTH.md) before configuring roles and [docs/DATA_SOURCES.md](docs/DATA_SOURCES.md) for source limitations.

## Operations and testing

The `migrate` service is the sole migration runner. `web` is stateless; PostgreSQL and Redis use persistent volumes. Use `docker compose up --scale web=3` to request three web containers. See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) and [docs/TESTING.md](docs/TESTING.md).

```sh
make test
make lint
```

`make seed-demo` explicitly creates synthetic sample users and scores. Never use those accounts as real candidate evidence. The synthetic pedigree training set is included only as a labeled fallback.
