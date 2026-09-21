# Data Quality and Lineage Workstream

This branch explores stronger guarantees around dataset provenance.

## Proposed lineage tuple

Every training dataset should be identifiable by:

`(dataset_name, semantic_version, content_hash, extraction_time, source_snapshot, schema_version)`

## Controls

- SHA-256 content hashes for immutable snapshots;
- schema evolution checks;
- point-in-time-safe joins;
- duplicate-key detection;
- target leakage review;
- row-count and prevalence deltas;
- quarantine paths for invalid batches.

## Production extension

Integrate DVC or lakehouse table versions so the MLflow run stores the exact data reference rather than only a filesystem path.
