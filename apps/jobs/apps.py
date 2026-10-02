from django.apps import AppConfig


class JobsConfig(AppConfig):
    """Recruiter-defined talent role requirements."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.jobs"
