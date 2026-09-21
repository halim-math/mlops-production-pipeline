# Data Subsystem

This package defines the boundary between raw information and model-ready features.

## Responsibilities
- online request schemas;
- batch dataset validation;
- feature transformation;
- compatibility checks between training and serving.

## Design rule
Feature logic used during training should be shared with serving wherever possible. Duplicated transformation code is a common source of training-serving skew.

## Validation layers
1. structural schema;
2. null and duplication checks;
3. domain/range validation;
4. target integrity;
5. statistical distribution checks;
6. lineage/version checks.

For real production data, add Great Expectations, Pandera, Deequ, or an equivalent data-quality system only where it improves operational clarity rather than duplicating existing checks.
