# Champion / Challenger Research Workstream

The challenger receives a shadow copy of production requests but cannot affect user decisions.

## Protocol
1. champion serves the official prediction
2. sanitized request is copied asynchronously to challenger
3. challenger output is stored with model/version metadata
4. delayed labels are joined later
5. paired metrics and calibration are computed
6. promotion requires predefined evidence

## Guardrails
- challenger failure must never fail the champion request
- shadow traffic must obey the same privacy policy
- inference cost must be monitored
- comparisons should be paired where possible
- promotion should account for uncertainty, not only point estimates

Advanced work can add conformal prediction, abstention policies and sequential testing.
