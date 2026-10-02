"""Candidate profile and evidence records."""

from django.conf import settings
from django.db import models


class CandidateProfile(models.Model):
    """Self-reported pedigree attributes, strictly separate from evidence signals."""

    class Tier(models.TextChoices):
        TIER_1 = "TIER_1", "Tier 1"
        TIER_2 = "TIER_2", "Tier 2"
        TIER_3 = "TIER_3", "Tier 3"
        UNKNOWN = "UNKNOWN", "Unknown"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="candidate_profile",
    )
    name = models.CharField(max_length=160, blank=True)
    gender = models.CharField(max_length=40, blank=True)
    college_tier = models.CharField(
        max_length=16, choices=Tier.choices, default=Tier.UNKNOWN
    )
    employer_brand = models.CharField(max_length=160, blank=True)
    region = models.CharField(max_length=100, blank=True)
    consent_given = models.BooleanField(default=False)
    self_reported = models.BooleanField(default=True)
    is_sample_data = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Candidate {self.user_id}"


class EvidenceLink(models.Model):
    """Candidate-provided source locator and ownership verification state."""

    class Source(models.TextChoices):
        GITHUB = "github", "GitHub"
        KAGGLE = "kaggle", "Kaggle"
        CERTIFICATE = "certificate", "Certificate"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="evidence_links",
    )
    source = models.CharField(max_length=20, choices=Source.choices)
    handle = models.CharField(max_length=200, blank=True)
    url = models.URLField(max_length=500, blank=True)
    verification_code = models.CharField(max_length=32, blank=True)
    ownership_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("user", "source", "handle", "url"), name="unique_evidence_link"
            )
        ]
