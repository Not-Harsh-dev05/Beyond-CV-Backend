"""Scoring administration routes."""

from django.urls import path
from .views import PedigreeTrainView

urlpatterns = [
    path(
        "admin/pedigree-model/train/",
        PedigreeTrainView.as_view(),
        name="pedigree-train",
    )
]
