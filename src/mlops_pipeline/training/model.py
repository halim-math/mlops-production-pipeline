from typing import Any

from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.pipeline import Pipeline

from mlops_pipeline.data.features import build_preprocessor


def build_model(params: dict[str, Any] | None = None) -> Pipeline:
    params = params or {}
    estimator = HistGradientBoostingClassifier(random_state=42, **params)
    return Pipeline(
        [
            ("features", build_preprocessor()),
            ("classifier", estimator),
        ]
    )
