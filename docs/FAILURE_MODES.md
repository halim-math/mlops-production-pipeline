# Failure Modes and Defenses

| Failure | Detection | Defense |
|---|---|---|
| Schema breaking change | validation errors | versioned contracts |
| Training-serving skew | offline/online parity test | shared feature code |
| Target leakage | suspicious offline gains | point-in-time review |
| Silent feature drift | PSI/distribution monitors | alerts + diagnosis |
| Concept drift | delayed-label metric decay | controlled retraining |
| Bad model promotion | model gates fail | CI promotion barrier |
| Dependency compromise | audit scan | pinned ranges + scanning |
| Artifact corruption | load/readiness failure | immutable registry |
| Latency regression | histogram/SLO alerts | load testing + rollback |
| Logging sensitive data | privacy review | pseudonymous telemetry |
| Pipeline non-reproducibility | rerun mismatch | lineage + seeded runs |
| Upstream missing values | data-quality report | ingestion quarantine |
| Class prevalence shift | target/data monitor | threshold recalibration |
| Retry storm | service metrics | bounded retries/backoff |
| Metric gaming | multi-metric review | explicit governance |
