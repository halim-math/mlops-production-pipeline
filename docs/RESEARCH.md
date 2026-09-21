# Research and Experiment Protocol

## Why this is more than a demo pipeline

Production ML systems fail differently from ordinary software. Their behavior depends on the joint distribution of code, data, labels, model parameters and operational traffic. This project treats those as versioned scientific objects.

## Experiment protocol

Every modeling experiment should record:

- immutable data version;
- Git commit;
- environment/dependency lock;
- random seed;
- feature schema version;
- hyperparameters;
- validation metrics;
- calibration metrics;
- subgroup metrics where legally and ethically appropriate;
- inference-cost measurements;
- quality-gate decision;
- model artifact digest.

A candidate that improves one metric but violates another system constraint is not automatically promoted.

## Recommended evaluation dimensions

### Predictive quality
- F1 for operating-point quality;
- ROC-AUC for ranking;
- Brier score for probabilistic calibration;
- precision/recall at business thresholds;
- confidence intervals from bootstrap resampling.

### Stability
- train/test performance gap;
- seed sensitivity;
- temporal split performance;
- feature perturbation robustness;
- missingness stress tests.

### Production behavior
- p50/p95/p99 latency;
- throughput;
- memory footprint;
- model load time;
- error rate;
- cold-start behavior.

### Distribution shift
- PSI for interpretable univariate monitoring;
- KS/Wasserstein tests for numeric variables;
- categorical population deltas;
- multivariate detectors for higher-order drift;
- delayed-label model-performance decay.

## Champion/challenger design

A mature deployment should support:
1. current champion receives production traffic;
2. challenger receives a shadow copy;
3. both produce predictions without challenger affecting decisions;
4. offline labels are joined later;
5. statistical tests compare performance and calibration;
6. promotion occurs only after predefined evidence thresholds.

## Reproducibility rule

An experiment is not reproducible merely because code is in Git. Reproduction requires **code + data + configuration + environment + random seeds + artifact lineage**.
