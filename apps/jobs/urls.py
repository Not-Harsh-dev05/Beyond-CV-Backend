"""Job and job-ranking routes."""

from django.urls import path
from .views import JobListCreateView

urlpatterns = [
    path("", JobListCreateView.as_view(), name="jobs"),
]
