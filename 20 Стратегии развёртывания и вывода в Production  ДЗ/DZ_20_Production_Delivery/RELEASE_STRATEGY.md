# Release Strategy — Canary

## Цель

Снизить blast radius нового AI-релиза, сохраняя предыдущую stable-версию доступной до полного promotion.

## State machine

```text
CANDIDATE_READY
→ STAGING_VALIDATED
→ CANARY_1
→ CANARY_5
→ CANARY_100
→ PROMOTED
```

Любой blocking failure:

```text
CANARY_* → ROLLBACK → STABLE_RESTORED → RCA
```

## Выбранный progressive-delivery механизм

```text
CI → Registry → Git desired state
                 ↓
              Argo CD
                 ↓
          Argo Rollouts CR
                 ↓
        Stable / Canary Services
                 ↓
 Traffic Router (NGINX/Istio/ALB/equivalent)
                 ↓
        1% → 5% → 100%
                 ↓
        AnalysisRun / Metrics
          ↓ PASS       ↓ FAIL
       PROMOTE         ABORT
```

Argo CD отвечает за GitOps reconciliation. Argo Rollouts отвечает за progressive delivery, traffic weights, pause/analysis и abort/promotion.

## Traffic policy

- 0%: candidate deployed but receives only synthetic/smoke traffic;
- 1%: first production exposure;
- 5%: expanded exposure after gate;
- 100%: full promotion after successful gate.

## Gate classes

- technical: availability, errors, latency;
- AI quality: task success, faithfulness/groundedness;
- security: leakage, secrets, unsafe output;
- economics: cost/request;
- operational: saturation, crash loops, dependency failures.

## Feature flags

Feature flags используются как дополнительный механизм отделения deploy от exposure. Они не заменяют Canary, но позволяют:
- включать новую функцию только выбранной группе;
- отключить feature без пересборки;
- отдельно переключать model/RAG route при совместимом контракте.

## Observation window

Фиксированное число минут не считается универсальным gate. Минимальное окно определяется объёмом данных:

`T_sample = N_required / (RPS × traffic_share)`.

После достижения sample requirement применяется metric gate; при необходимости добавляется минимальное wall-clock окно для покрытия warm-up/cache/load-cycle effects.

## Example project thresholds

These thresholds are design assumptions for this homework and are configuration-driven:

- p95 latency regression: <= 20% vs stable;
- AI quality relative degradation: <= 5%;
- cost/request regression: <= 20% unless approved;
- critical security/data-leak findings: 0.

Error-rate threshold should be tied to the service SLO and stable baseline rather than hard-coded globally.

## Rollback

Rollback is traffic-first:

1. send 100% traffic to stable;
2. stop candidate progression;
3. mark candidate FAILED;
4. revert desired deployment state to previous complete release bundle (app + model + RAG index + prompt/config);
5. keep evidence and telemetry;
6. open RCA;
7. fix and issue a new candidate version.

No rebuild of the previous version is required because the stable release uses immutable references.


## Strategy choice

Rolling и Blue-Green рассмотрены как альтернативы. Для учебного AI-service выбран Canary, потому что он ограничивает blast radius и соответствует прямому требованию OTUS 1% → 5% → 100%.

See: `DEPLOYMENT_STRATEGIES.md`.
