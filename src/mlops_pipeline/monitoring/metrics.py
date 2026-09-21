from prometheus_client import Counter, Gauge, Histogram

REQUESTS = Counter(
    "ml_inference_requests_total",
    "Total inference requests",
    labelnames=("status",),
)
LATENCY = Histogram(
    "ml_inference_latency_seconds",
    "Inference request latency",
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2, 5),
)
PREDICTION_RATE = Gauge(
    "ml_positive_prediction_rate",
    "Most recent exponentially smoothed positive prediction rate",
)
MODEL_INFO = Gauge(
    "ml_model_info",
    "Loaded model metadata",
    labelnames=("version",),
)
