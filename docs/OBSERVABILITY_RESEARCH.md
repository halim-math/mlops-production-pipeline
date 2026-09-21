# Observability and Drift Workstream

This branch extends monitoring beyond basic PSI.

## Layers

- univariate numeric drift;
- categorical distribution drift;
- multivariate drift;
- prediction distribution change;
- calibration drift;
- delayed-label accuracy decay;
- segment-specific degradation.

## Research questions

- Which drift metrics correlate with real performance loss?
- How stable are thresholds across seasonality?
- Can alerts be adapted to feature criticality?
- When should drift create a ticket versus page an operator?
- How should delayed labels be joined without temporal leakage?

A mature system separates detection, diagnosis and remediation.
