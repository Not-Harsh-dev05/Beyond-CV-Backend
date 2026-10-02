from django.apps import AppConfig
from django.conf import settings
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class ScoringConfig(AppConfig):
    """Evidence-only competence scoring and pedigree baseline."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.scoring"

    def ready(self):
        """Warn at startup when the production-trained baseline is not installed."""
        if not Path(settings.PEDIGREE_MODEL_PATH).exists():
            logger.warning(
                "pedigree_model_missing fallback=sample_synthetic_or_population_mean"
            )
