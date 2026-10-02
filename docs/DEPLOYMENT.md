# Deployment

## Compose stack

`docker compose up --build` starts Nginx, PostgreSQL, Redis, two declared web replicas, Celery worker and beat. The one-shot `migrate` service waits for DB and Redis health, then applies migrations and collects static assets before web/worker/beat start. Web replicas do not run migrations. Django/Gunicorn/Celery run as an unprivileged container user.

```sh
cp .env.example .env
# Replace SECRET_KEY, DB credentials, host list, CORS origins, and optional API credentials.
docker compose up --build
docker compose up --scale web=3
docker compose down
```

Compose deployment `replicas` declares two web instances; for regular Docker Compose use `--scale web=3` to choose a different count. The app keeps no local user/session/cache state. PostgreSQL and Redis have named persistent volumes; static files use a shared volume. Nginx resolves Docker's `web` service name dynamically, retries passive upstream failures, forwards request IDs, compresses responses, and sets browser security headers.

## Production checklist

- Use strong unique secrets, a managed PostgreSQL/Redis deployment, TLS at Nginx/load balancer, restricted CORS and valid `ALLOWED_HOSTS`.
- Configure GitHub and Kaggle credentials only if the corresponding source is enabled. Keep them out of images and logs.
- Ensure outbound network policy permits only required official APIs and certificate domains. URL fetcher validates host, DNS results, redirects, timeout and response size.
- Provide a representative, consented training CSV, run `train_pedigree_model`, and securely distribute the versioned model artifact. The local model artifact path defaults under `var/` and is intentionally gitignored; mount durable/shared read-only model storage if all workers must share it.
- Monitor worker queue latency, failed jobs, rate limits, DB/Redis health, and `X-Served-By`. Set up backups and log retention outside this app.

The Docker build downloads CPU PyTorch and the sentence-transformer model at build time. The local inference loader uses `local_files_only=True`; runtime model download is not attempted.
