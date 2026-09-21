# Monitoring Subsystem

Monitoring is split into three independent questions:

1. **Is the service healthy?**  
   Errors, latency, saturation and availability.

2. **Is the input/model behavior changing?**  
   Feature drift, prediction drift, calibration drift and model-version changes.

3. **Is the model still useful?**  
   Delayed-label performance and business outcome metrics.

Drift is evidence of change, not proof of model failure. Retraining should occur through the same validation and promotion controls as the original model.
