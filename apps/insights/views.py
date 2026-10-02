"""Administrator-only aggregate insights API."""

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from apps.accounts.permissions import IsAdmin
from apps.core.pagination import DefaultPagination
from .services import undervalued_skills


class UndervaluedSkillsView(APIView):
    """Return only groups that meet the configured minimum k."""

    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        data = undervalued_skills(
            request.query_params.get("region", ""), request.query_params.get("tier", "")
        )
        paginator = DefaultPagination()
        page = paginator.paginate_queryset(data, request, view=self)
        return paginator.get_paginated_response(page)
