# STEP 23 — DZ20 Production Delivery submission

Status: **READY FOR SUBMISSION / architecture package**. Course status remains **not submitted** until uploaded.

## Homework coverage

1. IaC — Terraform-style VPC/K8s/S3 design.
2. CI/CD — Commit → Build → Unit → Staging → E2E → Prod.
3. MLOps — data change → Airflow → retrain/reindex → eval → Model/Index Registry → delivery trigger.
4. Canary — 1% → 5% → 100% with rollback metrics.

## Source research

Argo CD:
- API server exposes sync/rollback and status operations;
- repository server generates Kubernetes manifests from Git revision/path/config;
- application controller continuously compares live state with Git desired state and reconciles drift.

Canary:
- gradual traffic exposure reduces release risk;
- stable can remain available while candidate traffic grows;
- rollback can be traffic redirection back to stable;
- Canary should not be conflated with A/B testing.

## Boundary

No claim is made that Argo CD, cloud Kubernetes, S3 or Canary runtime has already been deployed. The OTUS homework asks for pipeline architecture and release strategy.
