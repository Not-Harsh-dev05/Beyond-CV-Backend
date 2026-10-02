"""Celery ingestion task with retries and idempotent job state updates."""

import logging
from apps.scoring.competence import NoUsableSignals
from celery import shared_task
from django.utils import timezone
from .models import IngestionJob
from .services import process_candidate

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    autoretry_for=(TimeoutError,),
    retry_backoff=True,
    retry_jitter=True,
    max_retries=3,
    time_limit=300,
    soft_time_limit=240,
)
def run_ingestion(self, job_id: int):
    """Run ingestion for an existing pending/running job."""
    job = IngestionJob.objects.select_related("user").get(pk=job_id)
    if job.status == IngestionJob.Status.SUCCESS:
        return job.pk
    job.status = IngestionJob.Status.RUNNING
    job.started_at = job.started_at or timezone.now()
    job.save(update_fields=("status", "started_at"))
    try:
        process_candidate(job.user, ingestion_job=job)
    except NoUsableSignals as exc:
        logger.warning("ingestion_failed job_id=%s error=%s", job.pk, str(exc)[:200])
        job.status = IngestionJob.Status.FAILED
        job.error = str(exc)[:500]
    except Exception as exc:
        logger.warning("ingestion_retry job_id=%s error=%s", job.pk, str(exc)[:200])
        if self.request.retries < self.max_retries:
            raise self.retry(exc=exc, countdown=min(60, 2**self.request.retries))
        job.status = IngestionJob.Status.FAILED
        job.error = "Ingestion failed after repeated attempts."
    else:
        job.status = IngestionJob.Status.SUCCESS
        job.error = ""
    job.finished_at = timezone.now()
    job.save(update_fields=("status", "error", "finished_at"))
    return job.pk
