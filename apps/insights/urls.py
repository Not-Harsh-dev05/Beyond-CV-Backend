"""Aggregate insights routes."""

from django.urls import path
from .views import UndervaluedSkillsView

urlpatterns = [
    path(
        "undervalued-skills/",
        UndervaluedSkillsView.as_view(),
        name="undervalued-skills",
    )
]
