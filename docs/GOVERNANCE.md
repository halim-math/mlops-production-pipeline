# Model Governance

## Roles

- **Model author**: owns training code and evaluation evidence.
- **Reviewer**: validates methodology, leakage risk and reproducibility.
- **Platform owner**: owns deployment controls and observability.
- **Business owner**: defines acceptable operating thresholds and impact constraints.

## Promotion evidence

A production promotion should include:
- model version and immutable artifact digest;
- source Git SHA;
- data-version identifier;
- metric report;
- quality-gate output;
- security scan status;
- inference performance report;
- rollback target;
- reviewer approval.

## Risk controls

### Data
- schema validation;
- missingness bounds;
- duplication checks;
- target-prevalence checks;
- lineage/versioning.

### Model
- minimum validation quality;
- calibration threshold;
- overfit-gap threshold;
- robustness tests;
- documented intended use.

### Service
- typed payloads;
- health probes;
- constrained dependencies;
- non-root container;
- audit-friendly structured logs;
- metrics without raw sensitive inputs.

## Human oversight

Automatic retraining may create a candidate, but production promotion should remain policy-controlled. High-impact applications require stronger domain, fairness, legal and safety review than this generic reference implementation supplies.
