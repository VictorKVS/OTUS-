# STEP 22 — DZ18 IaC / CI/CD / DevSecOps Lab scaffold

Status: **DRAFT / M1**.

Created a runnable local lab that maps the course targets to local equivalents:

- VPC → Docker network;
- S3 → MinIO;
- Kubernetes cluster → Minikube;
- IaC → Terraform;
- CI/CD → GitHub Actions;
- DevSecOps → pytest/Bandit/Semgrep/pip-audit/detect-secrets/CycloneDX/Checkov/Trivy.

This step does **not** claim runtime success. Promotion to LAB/M1 requires local deployment and captured evidence.


## Shared Kubernetes lab decision

DZ18 does not create a second local Kubernetes learning stack. It reuses the Kubernetes-course baseline:

`Docker Desktop → kubectl → Minikube`.

The Kubernetes DZ1 exercises run on Minikube, and Architect DZ18 deploys its agent workload into the same runtime model. `kind` is not required by DZ18.
