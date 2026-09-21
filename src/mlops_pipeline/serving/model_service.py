from dataclasses import dataclass
from pathlib import Path

import joblib
import pandas as pd

from mlops_pipeline.data.schema import CustomerFeatures
from mlops_pipeline.settings import Settings


@dataclass
class ModelService:
    model: object
    version: str

    @classmethod
    def load(cls, settings: Settings) -> "ModelService":
        if settings.model_uri:
            import mlflow.pyfunc
            model = mlflow.pyfunc.load_model(settings.model_uri)
            version = settings.model_uri
        else:
            path = Path(settings.model_path)
            if not path.exists():
                raise FileNotFoundError(f"Model artifact does not exist: {path}")
            model = joblib.load(path)
            version = path.name
        return cls(model=model, version=version)

    def predict(self, features: CustomerFeatures) -> tuple[int, float]:
        frame = pd.DataFrame([features.model_dump(mode="json")])
        prediction = int(self.model.predict(frame)[0])
        if hasattr(self.model, "predict_proba"):
            probability = float(self.model.predict_proba(frame)[0, 1])
        else:
            probability = float(prediction)
        return prediction, probability
