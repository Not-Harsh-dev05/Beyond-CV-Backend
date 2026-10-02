"""Ingestion job state and source signal cache."""

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone
from apps.candidates.models import EvidenceLink


class IngestionJob(models.Model):
    """Deduplicated asynchronous processing request."""

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        RUNNING = "RUNNING", "Running"
        SUCCESS = "SUCCESS", "Success"
        FAILED = "FAILED", "Failed"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ingestion_jobs",
    )
    status = models.CharField(
        max_length=12, choices=Status.choices, default=Status.PENDING
    )
    dedupe_key = models.CharField(max_length=64, unique=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    error = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("user",),
                condition=Q(status__in=("PENDING", "RUNNING")),
                name="one_active_ingestion_job_per_candidate",
            )
        ]

    @property
    def active(self):
        """Whether the job can be reused as an active request."""
        return self.status in (self.Status.PENDING, self.Status.RUNNING)


class SignalSnapshot(models.Model):
    """Cached normalized source response with freshness metadata."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="signal_snapshots",
    )
    evidence_link = models.ForeignKey(
        EvidenceLink,
        on_delete=models.CASCADE,
        related_name="snapshots",
        null=True,
        blank=True,
    )
    source = models.CharField(max_length=32)
    payload = models.JSONField(default=dict)
    method = models.CharField(max_length=16, default="api")
    fetched_at = models.DateTimeField(default=timezone.now)
    ttl = models.DurationField()

    class Meta:
        indexes = [models.Index(fields=("user", "source", "-fetched_at"))]

    @property
    def fresh(self):
        """Return whether this snapshot is within its configured TTL."""
        return self.fetched_at + self.ttl > timezone.now()
