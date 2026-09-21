from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "local"
    log_level: str = "INFO"
    model_name: str = "churn-classifier"
    model_stage: str = "Production"
    model_uri: str | None = None
    model_path: Path = Path("artifacts/model.joblib")
    mlflow_tracking_uri: str = "http://localhost:5000"
    prediction_log_path: Path = Path("/tmp/predictions.jsonl")
    drift_threshold: float = 0.15
    min_model_f1: float = 0.72
    max_p95_latency_ms: float = 250.0

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
