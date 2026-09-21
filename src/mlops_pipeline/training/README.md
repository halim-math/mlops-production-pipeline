# Training Subsystem

The training code treats model development as a reproducible experiment.

A training run must be attributable to:
- source Git SHA;
- data version;
- configuration;
- seed;
- environment;
- metrics;
- model artifact;
- promotion decision.

The pipeline intentionally keeps preprocessing inside the sklearn `Pipeline` so transformations are fitted only on training data and are serialized together with the estimator.

Quality gates are policy, not merely metrics. A candidate that fails a gate is rejected before promotion.
