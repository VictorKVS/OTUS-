# ДЗ-20 · Автоматизация поставки AI-сервиса

**Сквозной проект:** Secure AI Knowledge Assistant  
**Диапазон:** идея → Lesson 20  
**Цель:** показать единый воспроизводимый путь от изменения кода/данных до безопасного production release.

---

## 1. Что строим

Ассистент отвечает на вопросы по корпоративной базе знаний. Он использует RAG, возвращает цитаты, соблюдает права доступа, фильтрует PII/опасные запросы, пишет telemetry и имеет версионированные app/model/index/prompt artifacts.

Простыми словами: пользователь задаёт вопрос; система ищет только разрешённые документы; модель формирует ответ; система проверяет ответ; каждый релиз можно точно воспроизвести или откатить.

## 2. Сквозная архитектура

```text
DATA / KNOWLEDGE CHANGE
        ↓
VALIDATE
        ↓
ORCHESTRATOR
        ↓
RETRAIN MODEL / REBUILD RAG INDEX
        ↓
EVALUATION + SECURITY GATES
        ↓
MODEL / INDEX REGISTRY
        ↓
RELEASE MANIFEST
        ↓
COMMIT
        ↓
BUILD IMAGE
        ↓
UNIT + DEVSECOPS TESTS
        ↓
STAGING
        ↓
E2E + AI EVAL
        ↓
GIT DESIRED STATE
        ↓
ARGO CD
        ↓
KUBERNETES
        ↓
CANARY 1%
        ↓
METRIC GATE
        ↓
CANARY 5%
        ↓
METRIC GATE
        ↓
100% + PROMOTE
```

## 3. Deployment strategies: почему выбран Canary

Урок 20 рассматривает Rolling, Blue-Green и Canary. В проекте они сравниваются отдельно, а для production plan выбран Canary: он соответствует заданию 1% → 5% → 100% и лучше ограничивает blast radius AI-релиза.

Важно: Argo CD обеспечивает GitOps reconciliation, но точное progressive traffic management выполняет Argo Rollouts (или эквивалентный controller) вместе с NGINX/Istio/ALB-class traffic router и metric analysis.

См. `20 Стратегии развёртывания и вывода в Production  ДЗ/DZ_20_Production_Delivery/DEPLOYMENT_STRATEGIES.md`.

## 4. Infrastructure as Code

Terraform-style IaC автоматически описывает сеть/VPC, Kubernetes cluster, object storage/S3, artifact registry и observability hooks.

| Resource | Назначение | Почему автоматизируем |
|---|---|---|
| VPC / network | сетевые границы | повторяемость и контроль |
| Kubernetes | runtime | масштабирование и rollout |
| S3/Object Storage | datasets/models/evidence | immutable/versioned artifacts |
| Artifact Registry | container images | точная версия приложения |
| Observability | metrics/logs/traces | release gates и RCA |

## 5. CI/CD

```text
Commit
→ Build Docker
→ Unit Tests
→ SAST/SCA/Secrets/SBOM/IaC/Container Scan
→ Deploy Staging
→ E2E
→ AI Regression
→ Create Release Manifest
→ Update Git Desired State
→ Argo CD
→ Production Canary
```

Критическая идея: CI производит проверенные immutable artifacts; CD не «ходит вручную в кластер», а меняет desired state в Git, после чего GitOps controller выполняет reconciliation.

## 6. MLOps integration

```text
Dataset / Knowledge Update
→ Data Validation
→ Pipeline Trigger
→ Retrain and/or Reindex
→ Evaluate
→ Model / Index Registry
→ Approved Version
→ Release Manifest
→ Delivery Pipeline
```

### Связь кода и модели

| Release field | Example |
|---|---|
| app image | `...@sha256:<digest>` |
| git commit | immutable SHA |
| model | registry URI + version + digest |
| RAG index | version |
| prompt/config | version |

Только полный комплект получает `RELEASE_ID`.

## 7. Canary strategy

Требование курса: **1% → 5% → 100%**.

```text
STABLE 100%
   ↓
CANDIDATE DEPLOYED / 0%
   ↓
1% REAL TRAFFIC
   ↓
GATE
   ↓
5%
   ↓
GATE
   ↓
100%
   ↓
PROMOTE CANDIDATE TO STABLE
```

Canary не равен A/B. Canary снижает blast radius релиза. A/B проверяет гипотезу и требует отдельного statistical design.

### Почему маленький canary полезен

Google SRE показывает простую модель: если дефект даёт 20% ошибок, а candidate получает 5% трафика, вклад этого дефекта в общий error rate примерно 1% при равномерной нагрузке. Это не универсальная гарантия, но понятное инженерное объяснение снижения blast radius.

## 8. Rollback

```text
BLOCKING GATE FAIL
→ ROUTE 100% TO STABLE
→ STOP CANDIDATE
→ REVERT GIT DESIRED STATE
→ ARGO CD RECONCILE
→ VERIFY STABLE
→ PRESERVE EVIDENCE
→ RCA
→ FIX
→ NEW CANDIDATE
```

| Gate | Что проверяем | Основание числа |
|---|---|---|
| error/availability | SLO + error budget + stable comparison | production SLO |
| p95 latency | stable vs candidate | NFR/SLO + measured baseline |
| AI quality | versioned golden set | eval baseline + CI |
| security | 0 critical confirmed events | blocking policy |
| cost/request | approved budget | FinOps/business NFR |

Числа без измерения production baseline не объявляются production thresholds.

## 9. Практическая calibration

В репозитории есть воспроизводимый controlled lab. При 10 000 synthetic requests на каждый вариант получено:

| Metric | Stable | Candidate |
|---|---:|---:|
| success | 99.58% | 99.49% |
| error | 0.42% | 0.51% |
| p95 | 319.01 ms | 330.78 ms |
| p99 | 402.64 ms | 416.47 ms |

Эти значения подтверждают работу метода сравнения, но честно маркируются как **LAB**, а не как production evidence.

## 10. Авторская модель поэтапного наращивания DevOps, Security и масштаба

В дополнение к обязательной схеме ДЗ проект использует собственную maturity-модель. Security начинается с требований и trust boundaries, а не только с отдельного security-урока. DevOps начинается с воспроизводимости и deployability, затем развивается до observability, IaC/CI/CD, MLOps и GitOps/Canary. Масштабирование выполняется по измеримому bottleneck/failure domain, а не по принципу «сразу микросервисы и Kubernetes».

Подробная схема: `AUTHORIAL_MATURITY_MODEL.md`.

## 11. Assurance Backbone — краеугольный контур обеспечения

Главный вывод Lesson 20 в сквозном проекте: инструменты сами по себе не обеспечивают production. Production обеспечивается цепочкой доказательств.

```text
REQ/NFR
→ ARCHITECTURE GATE
→ BUILD/SECURITY GATE
→ AI EVAL GATE
→ STAGING GATE
→ CANARY 1% GATE
→ CANARY 5% GATE
→ PROMOTION
```

Правило проекта: **NO EVIDENCE → NO PROMOTION**.

Каждый gate сохраняет evidence и имеет явный fail action. Благодаря этому Security, Quality, Observability, DevSecOps и SRE работают не как отдельные дисциплины, а как единый Assurance Backbone.

См. `projects/PROJECT_0_20_SECURE_AI_KNOWLEDGE_ASSISTANT/ASSURANCE_BACKBONE.md`.

## 12. Критерии OTUS

| Критерий | Как закрыт |
|---|---|
| Связь code ↔ Model Registry | Release Manifest |
| Тестирование + Canary/Blue-Green | Unit/E2E/AI/DevSecOps + Canary |
| Минимум ручных действий | IaC + CI/CD + MLOps + GitOps reconciliation |

## 13. Вывод

Получен единый delivery architecture: изменение кода, модели или базы знаний проходит проверяемый pipeline; app/model/RAG/prompt версии связаны в одном релизе; production rollout идёт постепенно; откат выполняется к уже известному stable release без пересборки.

## Источники

- OTUS Lesson 20 — формулировка домашнего задания и Canary 1% → 5% → 100%.
- Argo CD Architectural Overview: https://argo-cd.readthedocs.io/en/stable/operator-manual/architecture/
- Google SRE Workbook, Canarying Releases: https://sre.google/workbook/canarying-releases/
- Martin Fowler, Canary Release: https://martinfowler.com/bliki/CanaryRelease.html
- NIST AI RMF / GenAI Profile: https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence


## Lesson 20 audit

Полная матрица соответствия лекции и домашнему заданию: `20 Стратегии развёртывания и вывода в Production  ДЗ/DZ_20_Production_Delivery/LESSON20_COMPLETENESS_AUDIT.md`.
