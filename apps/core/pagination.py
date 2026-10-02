"""Standard pagination with enveloped responses."""

from rest_framework.pagination import PageNumberPagination
from .responses import success


class DefaultPagination(PageNumberPagination):
    """Page-number pagination for list endpoints."""

    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        rows = list(data)
        sources_used = sorted(
            {
                source
                for row in rows
                if isinstance(row, dict)
                for source in row.get("sources_used", [])
            }
        )
        sources_failed = [
            failure
            for row in rows
            if isinstance(row, dict)
            for failure in row.get("sources_failed", [])
        ]
        return success(
            {
                "count": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": rows,
            },
            request=self.request,
            sources_used=sources_used,
            sources_failed=sources_failed,
            is_sample_data=any(
                row.get("is_sample_data", False)
                for row in rows
                if isinstance(row, dict)
            ),
        )
