"""Recruiter ranking routes."""

from django.urls import path

from .views import JobRankingView

urlpatterns = [
    path("jobs/<int:job_id>/ranking/", JobRankingView.as_view(), name="job-ranking")
]
