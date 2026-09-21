import time
from contextlib import asynccontextmanager
from uuid import uuid4

import structlog
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from mlops_pipeline.data.schema import CustomerFeatures, PredictionResponse
from mlops_pipeline.logging import configure_logging
from mlops_pipeline.monitoring.metrics import LATENCY, MODEL_INFO, PREDICTION_RATE, REQUESTS
from mlops_pipeline.monitoring.prediction_log import append_prediction_event
from mlops_pipeline.serving.model_service import ModelService
from mlops_pipeline.settings import get_settings

settings = get_settings()
configure_logging(settings.log_level)
log = structlog.get_logger()
service: ModelService | None = None
_positive_ema = 0.0


@asynccontextmanager
async def lifespan(_: FastAPI):
    global service
    service = ModelService.load(settings)
    MODEL_INFO.labels(version=service.version).set(1)
    log.info("model_loaded", version=service.version)
    yield


app = FastAPI(
    title="Production ML Inference API",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health/live")
def liveness() -> dict[str, str]:
    return {"status": "alive"}


@app.get("/health/ready")
def readiness() -> dict[str, str]:
    if service is None:
        raise HTTPException(status_code=503, detail="model is not loaded")
    return {"status": "ready", "model_version": service.version}


@app.post("/v1/predict", response_model=PredictionResponse)
def predict(features: CustomerFeatures) -> PredictionResponse:
    global _positive_ema
    if service is None:
        raise HTTPException(status_code=503, detail="model is not loaded")

    request_id = str(uuid4())
    start = time.perf_counter()
    try:
        prediction, probability = service.predict(features)
        REQUESTS.labels(status="success").inc()
        _positive_ema = 0.95 * _positive_ema + 0.05 * prediction
        PREDICTION_RATE.set(_positive_ema)
        append_prediction_event(
            settings.prediction_log_path,
            request_id=request_id,
            prediction=prediction,
            probability=probability,
            model_version=service.version,
        )
        return PredictionResponse(
            prediction=prediction,
            probability=probability,
            model_version=service.version,
            request_id=request_id,
        )
    except Exception:
        REQUESTS.labels(status="error").inc()
        log.exception("prediction_failed", request_id=request_id)
        raise HTTPException(status_code=500, detail="inference failed") from None
    finally:
        LATENCY.observe(time.perf_counter() - start)


@app.get("/metrics")
def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
