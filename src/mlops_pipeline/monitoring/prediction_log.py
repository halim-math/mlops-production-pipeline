import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path


def pseudonymous_request_key(request_id: str) -> str:
    return hashlib.sha256(request_id.encode("utf-8")).hexdigest()[:16]


def append_prediction_event(
    path: Path,
    *,
    request_id: str,
    prediction: int,
    probability: float,
    model_version: str,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    event = {
        "timestamp": datetime.now(UTC).isoformat(),
        "request_key": pseudonymous_request_key(request_id),
        "prediction": prediction,
        "probability": probability,
        "model_version": model_version,
    }
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event) + "\n")
