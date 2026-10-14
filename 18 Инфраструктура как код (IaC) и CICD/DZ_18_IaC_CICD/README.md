# DZ 18 — Infrastructure as Code + CI/CD + DevSecOps

Статус: **ENGINEERING DRAFT / M1**. Runtime evidence ещё не зафиксирован.

## Цель

Собрать минимальный, воспроизводимый production-like контур для AI/agent service:

```text
VALIDATED DEV PACK
→ BUILD
→ TEST
→ EVAL/QUALITY GATE
→ DEVSECOPS GATES
→ SBOM
→ CONTAINER
→ TERRAFORM
→ LOCAL KUBERNETES
→ DEPLOY
→ VERIFY
→ EVIDENCE
```

## Что соответствует Lesson 18

Источник урока требует:

- Infrastructure as Code / Terraform;
- CI/CD с quality gates;
- базовую инфраструктуру: VPC, Kubernetes cluster, S3.

В локальном lab используются аналоги:

| Требование курса | Local lab |
|---|---|
| VPC | Docker network `father-dz18-vpc` |
| Kubernetes cluster | Minikube profile `father-dz18` |
| S3 | MinIO |
| CI/CD | GitHub Actions |
| Quality/Security gates | pytest, Bandit, Semgrep, pip-audit, detect-secrets, Checkov, Trivy |
| SBOM | CycloneDX |

Это локальный учебный контур. Для production VPC/S3/managed K8s должны быть реализованы конкретным cloud/on-prem provider и зафиксированы отдельным ADR.

## Структура

```text
DZ_18_IaC_CICD/
├── app/
├── tests/
├── terraform/local-lab/
├── minikube/
├── k8s/
├── security/
├── evidence/
├── scripts/
├── Dockerfile
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## Предварительные требования

- Docker Desktop;
- Python 3.12+;
- Terraform;
- minikube;
- kubectl.

## Локальный запуск

Из PowerShell:

```powershell
cd "G:\1\OTUS\18 Инфраструктура как код (IaC) и CICD\DZ_18_IaC_CICD"
powershell -ExecutionPolicy Bypass -File .\scripts\deploy_local.ps1
```

После успешного deploy:

```powershell
kubectl port-forward -n father-dz18 svc/father-agent 8089:8080
```

Во втором окне:

```powershell
Invoke-RestMethod http://127.0.0.1:8089/health
```

Ожидается:

```json
{"status":"ok","service":"father-dz18-agent"}
```

## Уничтожение lab

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\destroy_local.ps1
```

## Evidence rule

Наличие файлов не равно успешному ДЗ. После запуска сохраняем:

- `terraform validate`;
- `terraform plan/apply`;
- `minikube get clusters`;
- `kubectl get all -n father-dz18`;
- rollout status;
- `/health`;
- CI run result;
- SBOM/scan reports.

После этого Lesson 18 можно поднять с `draft/M1` до `lab/M1`.
