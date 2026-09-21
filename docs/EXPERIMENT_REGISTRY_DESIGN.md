# Experiment Registry Workstream

This branch deepens experiment reproducibility and model governance.

## Candidate lifecycle

`Created -> Evaluated -> Validated -> Approved -> Production -> Archived`

Each transition should be supported by evidence and recorded in the model registry.

## Required metadata

- Git commit;
- dataset version;
- feature schema version;
- Python/dependency lock digest;
- random seed;
- evaluation split definition;
- quality-gate decision;
- model artifact digest;
- reviewer identity for protected environments.

## Research extension

Add bootstrap confidence intervals and statistically compare a candidate against the current champion before promotion.
