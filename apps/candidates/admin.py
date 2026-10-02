"""Admin registrations for candidate data."""

from django.contrib import admin
from .models import CandidateProfile, EvidenceLink

admin.site.register(CandidateProfile)
admin.site.register(EvidenceLink)
