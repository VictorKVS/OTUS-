# Assurance Backbone · обеспечение разработки и релиза

## Идея

Архитектура, Security, Evaluation, Observability, DevSecOps и SRE не должны существовать отдельными «островами». Они образуют один контур обеспечения.

```text
REQUIREMENT
    ↓
DESIGN CONTROL
    ↓
IMPLEMENTATION CONTROL
    ↓
TEST / EVAL
    ↓
OBSERVABILITY
    ↓
RELEASE GATE
    ↓
PRODUCTION EVIDENCE
    ↓
FEEDBACK / RCA
    ↓
NEXT REQUIREMENT / ADR
```

## Четыре вида обеспечения

| Assurance plane | На что отвечает | Примеры evidence |
|---|---|---|
| Quality | работает ли функция и AI-качество | unit/E2E/golden-set/RAG eval |
| Security | не нарушает ли система security boundary | threat model, SAST/SCA, red-team, leakage tests |
| Reliability | можно ли безопасно эксплуатировать | SLO, load test, health, saturation, rollback drill |
| Reproducibility | можно ли повторить/объяснить релиз | Git SHA, digests, registry versions, SBOM, release manifest |

## Gate contract

Каждый gate имеет один стандартный контракт:

```yaml
gate:
  id:
  inputs:
  checks:
  metrics:
  thresholds:
  evidence:
  pass_action:
  fail_action:
  owner:
```

Так проект масштабируется без потери управляемости: новый механизм добавляется как block со своим contract/evidence и подключается к тому же Gate Engine.
