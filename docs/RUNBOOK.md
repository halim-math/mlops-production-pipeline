# Operations Runbook

## Service will not become ready

1. Check `/health/live`.
2. Check application logs for `model_loaded`.
3. Verify `MODEL_URI` or `MODEL_PATH`.
4. Confirm artifact permissions and network access.
5. Restore the last known-good model reference if the new artifact is invalid.

## Elevated 5xx inference rate

1. Correlate error count with deployment timestamp.
2. Inspect schema-validation versus internal inference failures.
3. Compare loaded model version with the release manifest.
4. Roll back immediately if errors breach the service SLO.
5. Preserve logs and metrics for post-incident analysis.

## Latency regression

1. Compare p50/p95/p99 before and after deployment.
2. Inspect CPU/memory pressure and container throttling.
3. Measure preprocessing and model prediction separately.
4. Validate batch/concurrency assumptions.
5. Roll back if the user-facing SLO is breached.

## Drift alarm

A drift alarm is **not automatically a retraining command**.

1. Verify the monitor is functioning and reference data is correct.
2. Identify which features shifted.
3. Check for upstream instrumentation or business-process changes.
4. If labels are available, measure actual model performance.
5. Retrain only through the normal candidate-validation path.
6. Record the decision, including a decision not to retrain.

## Suspected data leakage

1. Freeze model promotion.
2. Identify leakage source and affected data versions.
3. invalidate contaminated experiments.
4. rebuild datasets using point-in-time-safe joins.
5. rerun all validation from a clean lineage.

## Rollback

Rollback should restore:
- application image digest;
- model version;
- feature/schema contract;
- configuration;
- routing weights.

Never replace an artifact in place.
