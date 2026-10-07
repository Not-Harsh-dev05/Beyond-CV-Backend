"""Versioned API routes and schema endpoints."""

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from apps.core.views import health

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/health/", health, name="health"),
    path(
        "api/v1/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/v1/auth/", include("apps.accounts.urls")),
    path("api/v1/candidates/", include("apps.candidates.urls")),
    path("api/v1/ingestion/", include("apps.ingestion.urls")),
    path("api/v1/jobs/", include("apps.jobs.urls")),
    path("api/v1/", include("apps.ranking.urls")),
    path("api/v1/insights/", include("apps.insights.urls")),
    path("api/v1/", include("apps.scoring.urls")),
    path("", include("django_prometheus.urls")),
]
