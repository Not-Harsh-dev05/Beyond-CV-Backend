"""Celery task state transitions, terminal errors, and success idempotence."""

import pytest
from django.contrib.auth import get_user_model
from apps.candidates.models import CandidateProfile
from apps.ingestion.models import IngestionJob
from apps.ingestion.tasks import run_ingestion
from apps.scoring.competence import NoUsableSignals


@pytest.mark.django_db
def test_ingestion_task_success_and_duplicate_delivery_is_idempotent(monkeypatch):
    user = get_user_model().objects.create_user(
        email="taskok@example.test", username="taskok", password="StrongPass!234"
    )
    CandidateProfile.objects.create(user=user, consent_given=True)
    job = IngestionJob.objects.create(user=user, dedupe_key="task-success")
    monkeypatch.setattr(
        "apps.ingestion.tasks.process_candidate", lambda *_args, **_kwargs: None
    )
    run_ingestion.apply(args=[job.pk]).get()
    job.refresh_from_db()
    assert job.status == IngestionJob.Status.SUCCESS
    assert job.started_at and job.finished_at
    run_ingestion.apply(args=[job.pk]).get()
    assert job.status == IngestionJob.Status.SUCCESS


@pytest.mark.django_db
def test_ingestion_task_reports_zero_source_failure(monkeypatch):
    user = get_user_model().objects.create_user(
        email="taskfail@example.test", username="taskfail", password="StrongPass!234"
    )
    CandidateProfile.objects.create(user=user, consent_given=True)
    job = IngestionJob.objects.create(user=user, dedupe_key="task-failure")

    def no_signals(*_args, **_kwargs):
        raise NoUsableSignals("No evidence sources succeeded.")

    monkeypatch.setattr("apps.ingestion.tasks.process_candidate", no_signals)
    run_ingestion.apply(args=[job.pk]).get()
    job.refresh_from_db()
    assert job.status == IngestionJob.Status.FAILED
    assert "No evidence" in job.error
