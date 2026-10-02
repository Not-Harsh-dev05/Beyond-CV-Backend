"""Recruiter-only, consent-filtered role ranking API."""

from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from apps.accounts.permissions import IsRecruiter
from apps.jobs.models import JobRole
from apps.core.pagination import DefaultPagination
from .services import rank_candidates


class JobRankingView(APIView):
    """Return paginated explainable rankings for a role."""

    permission_classes = [IsAuthenticated, IsRecruiter]

    def get(self, request, job_id):
        job = get_object_or_404(JobRole, pk=job_id)
        rows = rank_candidates(job)
        paginator = DefaultPagination()
        selected = paginator.paginate_queryset(rows, request, view=self)
        return paginator.get_paginated_response(selected)
