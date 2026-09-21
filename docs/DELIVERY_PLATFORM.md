# CI/CD and Infrastructure Workstream

This branch focuses on delivery controls.

## Pipeline stages
1. source validation
2. lint/type checks
3. unit/property tests
4. dependency and static security scans
5. container build
6. integration tests
7. model validation
8. image signing and SBOM
9. staging deploy
10. smoke tests
11. protected production promotion

## Infrastructure direction
A cloud deployment can add Terraform for registry, managed compute, object storage, secrets, MLflow, monitoring, IAM and private networking. Cloud-specific resources are intentionally not hard-coded into main.
