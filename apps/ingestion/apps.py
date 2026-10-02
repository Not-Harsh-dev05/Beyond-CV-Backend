from django.apps import AppConfig


class IngestionConfig(AppConfig):
    """External evidence fetching and asynchronous jobs."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.ingestion"
