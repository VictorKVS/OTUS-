# FATHER DevOps / DevSecOps Factory — TARGET v0

Status: **TARGET / NOT RUNTIME-READY**.

Activation condition: Lesson 18 homework/lab must produce reproducible IaC + CI/CD evidence.

Input:
VALIDATED DEVELOPMENT PACK + SECURITY PROFILE + EVAL PROFILE + OBSERVABILITY/SLO + SIZING/INFERENCE PROFILE.

Pipeline:
REPO → BUILD → TEST → EVAL GATE → SAST/SCA/SECRETS → SBOM → CONTAINER/IAC SCAN → ARTIFACT → DEPLOY TARGET → VERIFY → EVIDENCE → RELEASE/ROLLBACK.

Deployment target selector:
- simple/single-service → Docker / Compose;
- multi-service, HA, autoscaling, production orchestration → Kubernetes.

Planned outputs:
- Dockerfile / compose;
- Terraform modules and environments;
- CI/CD workflows;
- security gates;
- SBOM and scan reports;
- registry references;
- Kubernetes/Helm only when selected;
- observability hooks;
- release manifest / rollback / evidence.

No component is considered production-ready until runtime evidence exists.
