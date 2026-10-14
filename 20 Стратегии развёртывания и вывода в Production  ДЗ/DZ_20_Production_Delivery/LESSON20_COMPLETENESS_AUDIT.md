# Lesson 20 completeness audit · production delivery

## Итог

Домашнее задание закрывает обязательные четыре пункта OTUS. После аудита добавлены недостающие элементы именно содержания Lesson 20: сравнение Rolling / Blue-Green / Canary, реальный progressive-delivery controller, traffic routing, metric analysis, feature flags, model/index extraction from registry, data validation/monitoring, release readiness и полный rollback release bundle.

## Матрица соответствия

| Lesson 20 item | Артефакт проекта | Статус |
|---|---|---|
| IaC: K8s + S3 | IAC_PSEUDOCODE.tf | COVERED |
| CI/CD: Commit → Build → Unit → Staging → E2E → Prod | DZ_20_SUBMISSION.md | COVERED |
| MLOps: dataset → trigger → retrain → registry → CI/CD | mlops/mlops-pipeline.yaml | COVERED |
| RAG: автоматическое обновление vector index | mlops/mlops-pipeline.yaml | COVERED |
| Model Registry ↔ application release | release/release-manifest.yaml | COVERED |
| Canary 1% → 5% → 100% | release/canary-policy.yaml | COVERED |
| rollback metrics | RELEASE_STRATEGY.md + canary policy | COVERED |
| release readiness checklist | READINESS_CHECKLIST.md | COVERED |
| rollback plan | ROLLBACK_PLAN.md | COVERED |
| Blue-Green / Canary / Rolling | DEPLOYMENT_STRATEGIES.md | ADDED |
| точное управление traffic split | Argo Rollouts + traffic router | ADDED |
| metric-driven promote/abort | AnalysisRun / Prometheus design | ADDED |
| data validation / Pandera | MLOps pipeline | COVERED / EXPLICIT |
| data/model drift / Evidently-style monitoring | MLOps pipeline | ADDED |
| feature flags | RELEASE_STRATEGY.md | ADDED |
| извлечение exact model from Registry at deploy | release manifest contract | ADDED |
| independent app/model/index versions | release manifest contract | COVERED |
| monorepo / independent versions concern | release identity separates artifacts | COVERED BY CONTRACT |

## Критическая архитектурная поправка

Argo CD отвечает за GitOps reconciliation: Git/OCI/Helm задаёт desired state, Application Controller синхронизирует его с Kubernetes.

Argo CD сам по себе не является точным механизмом Canary traffic splitting. Для 1% → 5% → 100% в проекте используется:

```text
GIT DESIRED STATE
      ↓
ARGO CD
      ↓
ROLL_OUT CR
      ↓
ARGO ROLLOUTS
      ↓
STABLE SERVICE + CANARY SERVICE
      ↓
TRAFFIC ROUTER
(NGINX / Istio / ALB / equivalent)
      ↓
1% → 5% → 100%
      ↓
ANALYSISRUN / PROMETHEUS
      ↓
PROMOTE OR ABORT
```

Это устраняет двусмысленность: GitOps deployment и progressive delivery являются связанными, но разными механизмами.

## Краеугольный принцип: Assurance Backbone

Все технологии в работе подчинены одной логике:

> **NO EVIDENCE → NO PROMOTION**

Каждый переход создаёт проверяемое evidence:

| Gate | Что доказываем | Evidence | Fail action |
|---|---|---|---|
| G0 Requirements | понятно, что и зачем строим | REQ/NFR/RISK | return to analysis |
| G1 Architecture | решение реализуемо и безопасно | C4/LLD/ADR/review | redesign |
| G2 Build | код собирается и базово корректен | unit/SAST/SCA/SBOM | block build |
| G3 AI quality/security | модель/RAG не деградировали | eval/security report | reject candidate |
| G4 Staging | интеграции работают вместе | E2E/load/smoke | block prod |
| G5 Canary 1% | ограниченный prod exposure безопасен | live metrics + analysis | abort to stable |
| G6 Canary 5% | расширенный exposure безопасен | live metrics + analysis | abort to stable |
| G7 100% | candidate можно сделать stable | release evidence bundle | rollback |

Эта линия обеспечения связывает требования, безопасность, качество, эксплуатацию и release engineering в один управляемый процесс.

## Научно/инженерно обоснованное окно Canary

Фиксированные «10 минут / 30 минут» удаляются как универсальные числа.

Минимальное время наблюдения выводится из требуемой выборки и фактического трафика:

```text
T_sample = N_required / (RPS × traffic_share)
```

Дополнительно окно должно покрывать эксплуатационную вариативность, если она существенна: warm-up, batching, cache, пики нагрузки, время внешних зависимостей.

Пример статистической проверки редкого критического события. Если считаем события независимыми Bernoulli и наблюдаем 0 событий, то для верхней границы 0.1% с confidence 95%:

```text
(1 - 0.001)^N ≤ 0.05
N ≥ ln(0.05) / ln(0.999)
N ≈ 2995
```

Это только пример метода. Конкретный production gate зависит от того, что считается «возможностью события» и насколько выполняется предположение независимости.

## Release unit и rollback

Откатывается не только Docker image. Единицей релиза является:

```text
APP IMAGE
+ MODEL DIGEST
+ RAG INDEX VERSION
+ PROMPT/CONFIG VERSION
+ SCHEMA/MIGRATION COMPATIBILITY
+ EVIDENCE BUNDLE
= RELEASE_ID
```

Rollback выполняется traffic-first, затем возвращает предыдущий release bundle. Любая stateful migration должна быть backward-compatible либо иметь отдельный tested rollback/expand-contract plan.
