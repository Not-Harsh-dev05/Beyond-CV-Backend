"""Candidate self-service routes."""

from django.urls import path
from .views import (
    CandidateMeView,
    EvidenceCreateView,
    EvidenceDetailView,
    CandidateScoreView,
)

urlpatterns = [
    path("me/", CandidateMeView.as_view(), name="candidate-me"),
    path("me/evidence/", EvidenceCreateView.as_view(), name="candidate-evidence"),
    path(
        "me/evidence/<int:evidence_id>/",
        EvidenceDetailView.as_view(),
        name="candidate-evidence-detail",
    ),
    path(
        "<int:candidate_id>/score/",
        CandidateScoreView.as_view(),
        name="candidate-score",
    ),
]
