# Serving Subsystem

The serving package exposes a versioned HTTP inference API.

## Endpoints
- `/health/live`: process health;
- `/health/ready`: model readiness;
- `/v1/predict`: prediction;
- `/metrics`: Prometheus exposition.

## Reliability principles
- fail readiness when no model is loaded;
- validate every payload;
- include model version in responses;
- record latency and failures;
- avoid logging raw sensitive features by default;
- keep model loading separate from request handling.

For high-throughput deployments, extend this layer with autoscaling, request batching, circuit breaking, canary routing and load tests.
