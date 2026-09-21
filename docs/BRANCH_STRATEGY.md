# Branch Strategy

The repository uses topic branches to make architectural concerns independently reviewable.

- `feature/data-quality-lineage` — data contracts, lineage and validation research.
- `feature/experiment-registry` — experiment tracking, registry and reproducibility.
- `feature/serving-platform` — scalable API serving and inference resilience.
- `feature/observability-drift` — telemetry, drift and performance monitoring.
- `ops/cicd-infrastructure` — CI/CD, containers and infrastructure automation.
- `research/champion-challenger` — shadow deployment, uncertainty and controlled promotion.

`main` is the integrated reference implementation. Topic branches are intentionally safe places for deeper prototypes before selected work is merged.
