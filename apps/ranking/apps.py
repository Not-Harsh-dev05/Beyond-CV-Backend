from django.apps import AppConfig


class RankingConfig(AppConfig):
    """Explainable candidate-to-role rankings."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.ranking"
