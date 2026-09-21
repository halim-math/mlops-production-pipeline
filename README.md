# MLOps Production Pipeline

A production-grade reference project for **training, versioning, testing, deploying and monitoring machine-learning models automatically from data ingestion through production inference**.

This repository is designed as a senior-level MLOps / Data Science portfolio project rather than a notebook demo. It treats code, data, model artifacts, runtime configuration, observability and governance as first-class production objects.

## What this project demonstrates

- reproducible model training;
- strict batch and online data contracts;
- experiment tracking and model registration with MLflow;
- model promotion quality gates;
- Dockerized FastAPI inference;
- liveness and readiness probes;
- Prometheus-compatible inference monitoring;
- privacy-conscious prediction telemetry;
- statistical drift detection;
- CI quality, typing, tests, dependency auditing and security scanning;
- reproducible model-validation workflows;
- operational runbooks and failure-mode analysis;
- governance and rollback principles;
- research paths for champion/challenger deployment and uncertainty-aware ML.

## Lifecycle

```text
Raw / versioned data
        |
        v
Data validation + schema contracts
        |
        v
Feature pipeline
        |
        v
Train candidate
        |
        +--> MLflow experiment lineage
        |
        v
Offline evaluation
        |
        v
Quality gates ---- fail ---> reject candidate
        |
       pass
        v
Registered model
        |
        v
Containerized FastAPI service
        |
        v
Production inference
        |
        +--> Prometheus service metrics
        +--> pseudonymous prediction telemetry
        +--> drift / delayed-performance monitoring
        |
        v
Controlled retraining and promotion
```

## Repository map

```text
.
├── .github/workflows/
│   ├── ci.yml
│   └── model-validation.yml
├── configs/
│   └── training.yaml
├── docs/
│   ├── ARCHITECTURE.md
│   ├── BRANCH_STRATEGY.md
│   ├── FAILURE_MODES.md
│   ├── GOVERNANCE.md
│   ├── RESEARCH.md
│   └── RUNBOOK.md
├── monitoring/
│   ├── alerts.yml
│   └── prometheus.yml
├── scripts/
│   └── generate_sample_data.py
├── src/mlops_pipeline/
│   ├── data/
│   ├── monitoring/
│   ├── serving/
│   ├── training/
│   ├── logging.py
│   ├── pipeline.py
│   └── settings.py
├── tests/
├── Dockerfile
├── docker-compose.yml
├── Makefile
└── pyproject.toml
```

## Quick start

### 1. Create an environment

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

### 2. Generate deterministic demonstration data

```bash
python scripts/generate_sample_data.py
```

### 3. Run the training pipeline

```bash
python -m mlops_pipeline.training.train \
  --config configs/training.yaml \
  --data data/processed/train.csv
```

A candidate is rejected automatically if it violates configured quality gates.

### 4. Run tests and engineering checks

```bash
make lint
make test
make security
```

### 5. Serve the validated artifact

```bash
uvicorn mlops_pipeline.serving.app:app --host 0.0.0.0 --port 8000
```

Health endpoints:

- `GET /health/live`
- `GET /health/ready`
- `GET /metrics`

Prediction endpoint:

```bash
curl -X POST http://localhost:8000/v1/predict \
  -H "Content-Type: application/json" \
  -d '{
    "tenure_months": 8,
    "monthly_spend": 129.50,
    "support_tickets": 4,
    "contract_type": "month-to-month"
  }'
```

## Model-quality gates

The baseline configuration evaluates:

| Gate | Purpose |
|---|---|
| minimum F1 | operating-point predictive quality |
| minimum ROC-AUC | ranking quality |
| maximum Brier score | probabilistic calibration |
| maximum train/test F1 gap | basic overfitting defense |

Production systems should add temporal validation, uncertainty intervals, subgroup analysis where appropriate, robustness tests and delayed-label evaluation.

## Observability philosophy

Operational monitoring is separated into three categories:

1. **service health** — availability, error rate and latency;
2. **data/model health** — feature drift, prediction shift and eventually delayed-label metrics;
3. **business health** — domain KPIs and decision impact.

A drift alert does not automatically mean the model is wrong. It initiates diagnosis and evidence gathering.

## Security and privacy defaults

- runtime container executes as a non-root user;
- CI includes static security and dependency audits;
- online payloads are validated before inference;
- default prediction telemetry does not store raw feature values;
- artifacts are intended to be immutable and versioned;
- promotion and rollback are explicit operational actions.

## Research-grade extensions

See [docs/RESEARCH.md](docs/RESEARCH.md) for the experiment protocol and deeper research directions, including:

- champion/challenger shadow inference;
- conformal prediction;
- uncertainty-aware abstention;
- multivariate drift;
- online calibration monitoring;
- point-in-time feature correctness;
- causal investigation of distribution shifts.

## Engineering branches

The repository is structured around six focused topic branches:

- `feature/data-quality-lineage`
- `feature/experiment-registry`
- `feature/serving-platform`
- `feature/observability-drift`
- `ops/cicd-infrastructure`
- `research/champion-challenger`

See [docs/BRANCH_STRATEGY.md](docs/BRANCH_STRATEGY.md).

## Production caveat

This is a realistic reference architecture, but no generic repository can supply organization-specific cloud credentials, production datasets, legal review, business thresholds, network topology or incident ownership. Those are intentionally represented through configuration and documented extension points rather than hard-coded assumptions.
