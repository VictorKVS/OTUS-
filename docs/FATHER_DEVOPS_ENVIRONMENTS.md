# FATHER DevOps & Environment Standard

Status: DESIGN BASELINE

## 1. Position in the factory

```text
FATHER CORE
→ ALINA / KNOWLEDGE
→ OSINT
→ FATHER LAB
→ DEVOPS / ENVIRONMENT PLATFORM
→ CONTAINERS
→ KUBERNETES
→ CI/CD / GITOPS
→ OBSERVABILITY / SRE
→ ISOLATION / SANDBOX
→ FUTURE CYBER RANGE
```

The DevOps platform is shared infrastructure, not a separate product.

## 2. Environment profiles

1. LOCAL DEV — developer workstation / WSL / local services.
2. CONTAINER DEV — Docker/Compose reproducible project stack.
3. K8S DEV — local Kubernetes/minikube environment.
4. TEST — automated integration/evaluation environment.
5. STAGING — production-like release-candidate environment.
6. PRODUCTION — controlled production runtime.
7. ISOLATED LAB — disposable restricted environment for risky tests.
8. CYBER RANGE — future profile, disabled until prerequisite gates pass.

## 3. Common platform capabilities

- container images and registries;
- Kubernetes workloads/services/networking/storage;
- CI/CD;
- GitOps;
- secrets management;
- artifact/model/prompt/dataset registries;
- PostgreSQL/vector/object storage;
- queues/event bus;
- observability;
- SRE/SLO/error budgets;
- FinOps;
- DevSecOps gates;
- sandboxing/isolation;
- backups/restore;
- policy-as-code;
- environment promotion.

## 4. Environment gates

- G-ENV-01 Reproducibility;
- G-ENV-02 Isolation;
- G-ENV-03 Observability;
- G-ENV-04 Rollback/Recovery;
- G-ENV-05 Security;
- G-ENV-06 Resource Control;
- G-ENV-07 Evidence;
- G-ENV-08 Lab Safety.

Detailed algorithms are defined in `FATHER_VERIFICATION_ALGORITHMS.md`.

## 5. Delivery chain

```text
CODE / CONFIG
→ BUILD
→ UNIT / CONTRACT
→ AI EVAL
→ SECURITY
→ ARTIFACT
→ DEV
→ TEST
→ STAGE
→ CANARY
→ PROD
→ OBSERVE
→ FEEDBACK
```

## 6. Kubernetes role

Kubernetes is one runtime profile, not the architecture itself.

FATHER must keep workload contracts portable enough to support:
- local/container execution;
- Kubernetes;
- future cloud/on-prem/hybrid placements.

Kubernetes-specific evidence includes:
- manifests/Helm/Kustomize or equivalent;
- RBAC;
- NetworkPolicy where required;
- resource requests/limits;
- readiness/liveness;
- storage class/persistence decisions;
- rollout/rollback evidence;
- logs/metrics/traces;
- security scan evidence.

## 7. Cyber Range prerequisite

Cyber Range is PLANNED and cannot be activated until:

- disposable environment creation is reproducible;
- network isolation is tested;
- permissions/RBAC are tested;
- secrets are isolated;
- telemetry is complete;
- snapshots/rollback/recreate are tested;
- quotas/timeouts are enforced;
- evidence is retained;
- emergency stop exists.

Until then the UI must show Cyber Range as PLANNED/DISABLED.
