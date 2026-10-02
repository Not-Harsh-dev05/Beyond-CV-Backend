"""Admin registration for score results."""

from django.contrib import admin
from .models import ScoreResult

admin.site.register(ScoreResult)
