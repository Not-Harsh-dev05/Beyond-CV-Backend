"""Ridge baseline trained exclusively on college tier and employer brand."""

import logging
from pathlib import Path
import joblib
import pandas as pd
from django.conf import settings
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

logger = logging.getLogger(__name__)
FEATURES = ["college_tier", "employer_brand"]
TARGET = "competence"
SAMPLE_FILE = Path(__file__).parent / "data" / "pedigree_train_SAMPLE_SYNTHETIC.csv"


def train_model(data_path: str, output_path: str | None = None) -> str:
    """Train and persist a versioned artifact using only the two pedigree columns."""
    data = pd.read_csv(data_path)
    missing = set(FEATURES + [TARGET]) - set(data.columns)
    if missing:
        raise ValueError(
            f"Training CSV is missing required columns: {', '.join(sorted(missing))}"
        )
    if data.empty:
        raise ValueError("Training CSV must contain at least one record.")
    model = Pipeline(
        [
            (
                "features",
                ColumnTransformer(
                    [("categorical", OneHotEncoder(handle_unknown="ignore"), FEATURES)]
                ),
            ),
            ("regressor", Ridge(alpha=1.0)),
        ]
    )
    model.fit(data[FEATURES].fillna("UNKNOWN").astype(str), data[TARGET].astype(float))
    target = Path(output_path or settings.PEDIGREE_MODEL_PATH)
    target.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"version": "v1", "model": model}, target)
    return str(target)


class PedigreeBaseline:
    """Predict a baseline with an explicit source and warning for synthetic fallback."""

    def __init__(self, model_path=None):
        self.model_path = Path(model_path or settings.PEDIGREE_MODEL_PATH)

    def predict(self, college_tier: str, employer_brand: str) -> dict:
        """Predict baseline from pedigree inputs only, with robust fallback."""
        data = pd.DataFrame(
            [
                {
                    "college_tier": college_tier or "UNKNOWN",
                    "employer_brand": employer_brand or "UNKNOWN",
                }
            ]
        )
        if self.model_path.exists():
            artifact = joblib.load(self.model_path)
            model = artifact.get("model") if isinstance(artifact, dict) else artifact
            return {
                "score": round(float(model.predict(data[FEATURES])[0]), 2),
                "source": "trained_model",
                "warning": "",
            }
        try:
            sample = pd.read_csv(SAMPLE_FILE)
            model = Pipeline(
                [
                    (
                        "features",
                        ColumnTransformer(
                            [
                                (
                                    "categorical",
                                    OneHotEncoder(handle_unknown="ignore"),
                                    FEATURES,
                                )
                            ]
                        ),
                    ),
                    ("regressor", Ridge(alpha=1.0)),
                ]
            )
            model.fit(
                sample[FEATURES].fillna("UNKNOWN").astype(str),
                sample[TARGET].astype(float),
            )
            logger.warning("pedigree_model_missing using synthetic sample fallback")
            score = float(model.predict(data[FEATURES])[0])
            source = "sample_synthetic"
        except (OSError, ValueError, KeyError):
            logger.exception("pedigree_sample_unavailable using population mean")
            score, source = 50.0, "population_mean"
        return {
            "score": round(max(0.0, min(100.0, score)), 2),
            "source": source,
            "warning": (
                "Pedigree baseline uses a synthetic sample model and is not trained "
                "on representative production data."
            ),
        }
