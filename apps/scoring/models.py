"""Persisted explainable candidate scores."""

from django.conf import settings
from django.db import models


class ScoreResult(models.Model):
    """A score and provenance snapshot produced from live evidence."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="scores"
    )
    ingestion_job = models.OneToOneField(
        "ingestion.IngestionJob",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="score_result",
    )
    competence = models.FloatField()
    baseline = models.FloatField()
    delta = models.FloatField()
    baseline_source = models.CharField(max_length=32)
    warning = models.CharField(max_length=300, blank=True)
    breakdown = models.JSONField(default=dict)
    sources_used = models.JSONField(default=list)
    sources_failed = models.JSONField(default=list)
    ownership_verified = models.BooleanField(default=False)
    is_sample_data = models.BooleanField(default=False)
    computed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-computed_at"]
