# ДЗ-20 — Автоматизация поставки: IaC, CI/CD и MLOps-конвейеры

**Курс:** AI Architect  
**Урок:** 20 · Стратегии развёртывания и вывода в Production  
**Статус:** готово к сдаче как архитектурный проект; runtime evidence развивается отдельно.

## 1. Infrastructure as Code

Terraform описывает инфраструктуру декларативно:

```text
NETWORK / VPC
      ↓
KUBERNETES CLUSTER
      ↓
OBJECT STORAGE / S3
      ↓
CONTAINER / ARTIFACT REGISTRY
      ↓
OBSERVABILITY
```

В локальном учебном контуре это может отображаться как Docker network + Minikube + MinIO. В production конкретные VPC/K8s/S3 выбираются под cloud/on-prem.

См. `IAC_PSEUDOCODE.tf`.

## 2. CI/CD Pipeline

```text
COMMIT
  ↓
BUILD DOCKER
  ↓
UNIT TESTS
  ↓
QUALITY + DEVSECOPS GATES
  ↓
PUSH IMMUTABLE IMAGE
  ↓
DEPLOY STAGING
  ↓
E2E + AI EVAL
  ↓
CREATE RELEASE MANIFEST
  ↓
UPDATE GIT DESIRED STATE
  ↓
ARGO CD SYNC
  ↓
CANARY PROD
```

Argo CD применяется как GitOps CD: Git хранит desired state; Argo CD синхронизирует Kubernetes с этим состоянием.

## 3. MLOps Integration

```text
DATASET / KNOWLEDGE CHANGE
  ↓
VALIDATION
  ↓
AIRFLOW / PIPELINE TRIGGER
  ↓
RETRAIN MODEL
  +/or
REBUILD RAG INDEX
  ↓
EVALUATION
  ↓
MODEL REGISTRY / INDEX REGISTRY
  ↓
APPROVED VERSION
  ↓
RELEASE MANIFEST
  ↓
TRIGGER DELIVERY PIPELINE
```

Ключевой контракт релиза:

```text
APPLICATION IMAGE DIGEST
+
MODEL REGISTRY URI / VERSION
+
RAG INDEX VERSION
+
PROMPT / CONFIG VERSION
=
ONE RELEASE
```

Это обеспечивает требуемую связь между кодом приложения и model artifact.

## 4. Canary Release

Stable остаётся работающей версией до завершения раскатки.

```text
STABLE 100%
   ↓
DEPLOY CANDIDATE, 0% TRAFFIC
   ↓
CANARY 1%
   ↓ gate
CANARY 5%
   ↓ gate
CANARY 100%
   ↓
PROMOTE CANDIDATE → STABLE
```

Если gate не пройден:

```text
FAIL
 ↓
ROUTE 100% → PREVIOUS STABLE
 ↓
MARK RELEASE FAILED
 ↓
RESTORE PREVIOUS DESIRED STATE
 ↓
RCA / FIX / NEW RELEASE
```

### Rollback metrics

Следующие значения — **проектные пороги этого ДЗ**, а не значения OTUS:

| Signal | Rollback condition |
|---|---|
| Availability | readiness/liveness failure |
| Error rate | candidate materially worse than stable or > agreed SLO |
| p95 latency | >20% regression vs stable |
| AI task success / quality | >5% relative degradation |
| Faithfulness / groundedness | below approved release threshold |
| Unsafe output / guardrail | any critical security violation |
| Data leakage / secrets | any confirmed critical event |
| Cost/request | >20% regression without approved benefit |

Критические security/data-leak события останавливают rollout независимо от средних метрик.

## GitOps / Argo CD

В выбранной архитектуре:

```text
CI
 ↓
ARTIFACTS
 ↓
UPDATE DEPLOYMENT REPO
 ↓
ARGO CD
 ↓
KUBERNETES
```

CI не должен вручную изменять production cluster. Он публикует immutable artifacts и изменяет desired state. Argo CD выполняет reconciliation.

## Canary vs A/B

Canary используется для **снижения риска релиза** и обнаружения регрессий.

A/B используется для **проверки продуктовой/ML-гипотезы**.

Механизм traffic split может быть похож, но решение о продвижении различается: Canary опирается прежде всего на safety/reliability/quality gates, A/B — на статистический результат бизнес-гипотезы.

## Критерии OTUS

### 1. Интеграция — выполнено

`release-manifest.yaml` связывает:
- image digest;
- model registry URI/version;
- RAG index;
- prompt/config.

### 2. Безопасность релиза — выполнено

Pipeline содержит:
- unit tests;
- E2E;
- AI evaluation;
- DevSecOps gates;
- Canary 1% → 5% → 100%;
- automatic rollback contract.

### 3. Автоматизация — выполнено в проекте

Ручное действие требуется только для policy-defined approval, если оно включено. Остальной путь предполагается автоматическим:

`commit/data change → pipeline → registry → Git desired state → Argo CD → Canary gates → promote/rollback`.

## Что сдаём

1. Эту схему/описание.
2. `IAC_PSEUDOCODE.tf`.
3. `release/release-manifest.yaml`.
4. `release/canary-policy.yaml`.
5. `mlops/mlops-pipeline.yaml`.
6. `RELEASE_STRATEGY.md`.

