"""Admin registrations for ingestion records."""

from django.contrib import admin
from .models import IngestionJob, SignalSnapshot

admin.site.register(IngestionJob)
admin.site.register(SignalSnapshot)
