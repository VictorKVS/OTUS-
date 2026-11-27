# SADEQ Эскизный проект / ConOps V0.1
**Статус:** DESIGN DRAFT — без согласования заказчика и инженерных испытаний. **База:** IDEA+ v0.3 / TZ v0.3, рыночная справка SADEQ-ANALOG-001.

Этот комплект является **первым рабочим наполнением эскизного проекта**, а не оформленным и принятым комплектом по ГОСТ. Номера ЭП-* — внутренние. При выпуске оформленных документов требуется проверка применимой редакции ГОСТ 34.201-2020 и ГОСТ Р 59793-2021, списка документов, штампов/согласования и договора.

## Состав
| ID | Документ | Статус |
|---|---|---|
| ЭП-001 | [ConOps — сценарий предприятия и операционная модель](EP-001_CONOPS_ENTERPRISE_OPERATIONS.md) | DRAFT |
| ЭП-002 | [Сценарии, бизнес-исключения и критерии приёмки](EP-002_USE_CASES_AND_ACCEPTANCE.md) | DRAFT |
| ЭП-003 | [HLD/C4, роли, блоки и границы доверия](EP-003_HLD_BOUNDARIES.md) | DRAFT |
| ЭП-004 | [ADR — альтернативы и архитектурные решения](EP-004_ADR_ARCHITECTURE_CHOICES.md) | PROPOSED |
| ЭП-005 | [Матрица требований и инженерных доказательств](EP-005_TRACEABILITY_AND_GATES.md) | DRAFT |
| Визуализация | [Концепция рабочего процесса](diagrams/CONOPS_OPERATIONS_FLOW.mmd) | CONCEPT |
| Визуализация | [Trust/data boundary](diagrams/SECURITY_BOUNDARIES.mmd) | CONCEPT |

## Ссылки на основания
- [IDEA+ v0.3](../IDEA_PLUS_REBASELINE_V03/01_IDEA_PLUS_REBASELINE.md)
- [Техническое задание 0.3](../IDEA_PLUS_REBASELINE_V03/02_TECHNICAL_ASSIGNMENT_GOST_34_602.md)
- [Паспорт размещения](../IDEA_PLUS_REBASELINE_V03/05_ENTERPRISE_DEPLOYMENT_HORIZON.md)
- [Учебный корпус](../IDEA_PLUS_REBASELINE_V03/06_AGENT_KNOWLEDGE_CURRICULUM.md)
- [POLYGON и допуск](../IDEA_PLUS_REBASELINE_V03/07_AGENT_TRAINING_AND_QUALIFICATION.md)
- [Мировые аналоги](../IDEA_PLUS_REBASELINE_V03/08_WORLD_ANALOGS_AND_BENCHMARKS.md)

## Неизменяемый смысл проекта
Строим **один работающий P0**, затем квалифицируем его и расширяем до P1 (GraphRAG, три профиля, Kubernetes) для цели OTUS. Нет реального заказчика, пилота, производственных KPI, государственной сертификации или заключения POLYGON.