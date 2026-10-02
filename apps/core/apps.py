from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Shared API infrastructure."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core"
