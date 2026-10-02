"""Recruiter job roles and skill requirements."""

from django.conf import settings
from django.db import models


class JobRole(models.Model):
    """Role used to compute transparent evidence fit rankings."""

    recruiter = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="job_roles"
    )
    title = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    required_skills = models.JSONField(default=list)
    skill_weights = models.JSONField(default=dict, blank=True)
    is_sample_data = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
