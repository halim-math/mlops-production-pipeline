# Production Architecture

## Objective

This repository demonstrates the complete operational lifecycle of a supervised machine-learning system:

**ingest -> validate -> version -> train -> evaluate -> register -> approve -> deploy -> observe -> detect drift -> retrain**

The architecture deliberately separates **training-time**, **control-plane**, and **serving-time** responsibilities so that failures are isolated and auditable.

## Logical components

1. **Data contract layer**
   - Pydantic schemas protect online requests.
   - Batch validation rejects malformed or suspicious training data.
   - DVC-compatible paths enable immutable dataset snapshots.

2. **Training layer**
   - Deterministic train/test splitting.
   - Leakage-safe sklearn Pipeline.
   - Explicit calibration-sensitive and ranking metrics.
   - Hard model-quality gates prevent accidental promotion.

3. **Experiment and registry layer**
   - MLflow stores parameters, metrics, artifacts, lineage and registered models.
   - Every candidate has reproducible evidence.

4. **Serving layer**
   - FastAPI exposes versioned prediction endpoints.
   - Liveness and readiness are separated.
   - Model metadata is exposed as monitoring state, not user payload.

5. **Observability layer**
   - Prometheus-compatible counters, latency histograms and prediction-rate gauges.
   - Prediction events are pseudonymized and intentionally exclude raw customer features.
   - Drift analysis is performed against a reference distribution.

6. **Delivery layer**
   - GitHub Actions executes linting, type checks, tests, security scans and container builds.
   - Promotion validation is an explicit workflow.

## Production invariants

- No model is considered deployable unless quality gates pass.
- The online feature contract must remain backward compatible across a deployment window.
- A service is not ready until a model has been loaded.
- Raw request data is not written to the default prediction telemetry stream.
- Artifacts are immutable; promotions move references, not files.
- Rollback means restoring a previously validated model version and application image.

## Research directions

The repository can be extended with:
- delayed-label performance monitoring;
- conformal prediction and abstention;
- champion/challenger shadow inference;
- causal drift diagnostics;
- feature-store point-in-time correctness;
- online calibration monitoring;
- uncertainty-aware retraining policies;
- model-card and dataset-card generation.
