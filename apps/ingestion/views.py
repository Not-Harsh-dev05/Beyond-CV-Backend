"""Thin API views for ingestion job creation and polling."""

from datetime import timedelta

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from apps.accounts.permissions import IsCandidateOwner
from apps.core.responses import failure, success
from apps.candidates.models import CandidateProfile
from .models import IngestionJob
from .services import create_ingestion_job
from .tasks import run_ingestion


def _truthy(value) -> bool:
    """Interpret JSON booleans and common string forms of a flag."""
    if isinstance(value, str):
        return value.strip().lower() in ("1", "true", "yes")
    return bool(value)


class IngestionJobsView(APIView):
    """Submit an asynchronous job for a consenting candidate."""

    permission_classes = [IsAuthenticated, IsCandidateOwner]

    def post(self, request):
        if request.user.role != "CANDIDATE":
            return failure(
                "forbidden",
                "Only candidates can submit ingestion jobs.",
                status=403,
                request=request,
            )
        profile = CandidateProfile.objects.filter(user=request.user).first()
        if not profile or not profile.consent_given:
            return failure(
                "consent_required",
                "Consent is required before evidence ingestion.",
                status=403,
                request=request,
            )
        if profile.is_sample_data:
            return failure(
                "sample_data_read_only",
                "Synthetic demo evidence cannot be ingested as live evidence.",
                status=403,
                request=request,
            )
        force_refresh = _truthy(request.data.get("refresh"))
        if force_refresh:
            cutoff = timezone.now() - timedelta(
                minutes=settings.INGESTION_MIN_REFRESH_MINUTES
            )
            if IngestionJob.objects.filter(
                user=request.user,
                status=IngestionJob.Status.SUCCESS,
                finished_at__gte=cutoff,
            ).exists():
                return failure(
                    "refresh_too_soon",
                    "Evidence was refreshed recently; try again in a few minutes.",
                    status=429,
                    request=request,
                )
        job, created = create_ingestion_job(request.user)
        if created:
            run_ingestion.delay(job.pk, force_refresh)
        return success(
            {"job_id": job.pk, "status": job.status}, status=202, request=request
        )


class IngestionJobDetailView(APIView):
    """Poll only a job owned by the requesting candidate or accessible to an admin."""

    permission_classes = [IsAuthenticated, IsCandidateOwner]

    def get(self, request, job_id):
        job = get_object_or_404(IngestionJob, pk=job_id)
        self.check_object_permissions(request, job)
        return success(
            {
                "job_id": job.pk,
                "status": job.status,
                "started_at": job.started_at,
                "finished_at": job.finished_at,
                "error": job.error or None,
            },
            request=request,
        )
