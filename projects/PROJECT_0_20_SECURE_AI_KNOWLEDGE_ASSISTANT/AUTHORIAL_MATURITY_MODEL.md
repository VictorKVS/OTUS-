# Авторская модель поэтапного наращивания DevOps, Security и масштаба

## Зачем этот слой

OTUS задаёт обязательные технологии и практики по урокам. В сквозном проекте добавлена собственная методика: capability появляется не «по номеру урока», а тогда, когда возникает соответствующий риск, зависимость или эксплуатационная потребность.

Это позволяет ответить на три практических вопроса:

1. Когда реально начинает работать Security?
2. Когда проекту действительно нужен DevOps/DevSecOps?
3. Как масштабировать систему без преждевременного усложнения?

## Security как непрерывный поток

| Фазы | Security capability | Смысл |
|---|---|---|
| 0-3 | security assumptions, data restrictions, critical risks | безопасность входит в требования |
| 4-5 | trust boundaries, auth context, policy checks, failure paths | архитектура задаёт точки контроля |
| 6-12 | RAG ACL, provenance, integration/data policies | защищаются реальные пути к данным |
| 13-14 | security evaluation, threat model, red-team cases, controls | контроли становятся проверяемыми |
| 18 | SAST/SCA/secrets/SBOM/IaC/container scans | проверки становятся blocking CI/CD gates |
| 20 | release security gate + rollback | критическая регрессия останавливает rollout |

Это проектная реализация shift-left подхода. NIST SSDF рекомендует интегрировать secure-development practices в используемый SDLC; DORA также рассматривает security collaboration/testing как практики, проходящие через разработку.

## DevOps maturity D0-D5

| Level | Фазы | Минимальный механизм | Что доказывает |
|---|---|---|---|
| D0 | 0-3 | Git, versioning, DoD, reproducible config | проект воспроизводим |
| D1 | 4-7 | deployability, health/config contracts, container-ready boundaries | архитектура готова к automation |
| D2 | 8-15 | tests, evidence, observability, SLO candidates | решения можно принимать по данным |
| D3 | 16-18 | capacity model, IaC, CI/CD, DevSecOps | поставка воспроизводима |
| D4 | 19 | Model/Index Registry, MLOps triggers | AI lifecycle воспроизводим |
| D5 | 20 | GitOps, Canary, rollback, release evidence | production release управляем |

DevOps поэтому не «начинается на уроке 18». На 18-м происходит промышленная автоматизация уже подготовленной архитектуры.

## Scaling ladder

| Stage | Architecture | Добавляем | Gate |
|---|---|---|---|
| Research | один процесс / локальный прототип | минимум кода, измеримость гипотезы | понятна ценность и данные |
| PoC | простая deployable сборка | tests + versioning + basic eval | техническая гипотеза подтверждена |
| MVP | контракты и разделённые компоненты | CI, security baseline, telemetry | пользовательский сценарий стабилен |
| Pilot | staging + production-like runtime | IaC, SLO, capacity tests, rollback drill | подтверждена эксплуатационная готовность |
| Production | GitOps + versioned artifacts | Canary, registry, blocking gates | релиз проходит gates |
| Scale | выборочное горизонтальное масштабирование | autoscaling/HA/partitioning только для bottleneck | метрики доказывают необходимость |

Главный принцип: масштабируется не «весь проект», а доказанный bottleneck или отдельный failure/security domain.

## Block/Slot architecture

Проект хранит стабильные роли:

- MODEL_SLOT;
- RAG_SLOT;
- EVALUATOR_SLOT;
- SECURITY_SLOT;
- OBSERVABILITY_SLOT;
- DEPLOYMENT_SLOT.

В каждый slot можно вставить совместимый versioned block. Block должен включать:

```text
CODE
+ CONFIG
+ INPUT/OUTPUT CONTRACT
+ TESTS
+ SECURITY REQUIREMENTS
+ METRICS
+ VERSION
+ ROLLBACK POLICY
```

Это позволяет менять модель, RAG, evaluator или deployment-механизм без перестройки всей системы и использовать одинаковые блоки в разных проектах.

## Что является авторским расширением

| Элемент | Происхождение |
|---|---|
| Canary 1% -> 5% -> 100% | OTUS |
| IaC + CI/CD + MLOps + Model Registry | OTUS |
| Security stream 0-20 | авторская проектная схема, совместимая с SSDF/DORA |
| DevOps maturity D0-D5 | авторская модель |
| Research -> PoC -> MVP -> Pilot -> Production -> Scale | авторская модель |
| Block/Slot architecture | FATHER project model |
| COURSE/SOURCE/LAB/PROD provenance | авторская evidence policy |
| release identity: app + model + RAG + prompt/config | авторский release contract |

Эти элементы являются инженерной методикой проекта, а не заявлением о создании нового научного стандарта.
