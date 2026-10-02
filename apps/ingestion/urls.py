"""Ingestion submission and job polling routes."""

from django.urls import path
from .views import IngestionJobsView, IngestionJobDetailView

urlpatterns = [
    path("jobs/", IngestionJobsView.as_view(), name="ingestion-jobs"),
    path("jobs/<int:job_id>/", IngestionJobDetailView.as_view(), name="ingestion-job"),
]
