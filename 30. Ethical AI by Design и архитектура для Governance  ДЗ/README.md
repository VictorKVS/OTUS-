# Урок 30. Model Cards и FinOps

## Цель

Связать прозрачность модели, доказательства качества, риски и стоимость эксплуатации в одном выпускном gate.

## Цепочка

`MODEL + DATA → EVALUATION → RISKS/CONTROLS → MODEL CARD → UNIT ECONOMICS → RELEASE/REJECT`

## Артефакты

- `MODEL_CARD_TEMPLATE.md` — расширенный шаблон Model Card;
- `FINOPS_CHECKLIST.md` — Inform → Optimize → Operate;
- `SOURCES.md` — первоисточники и атрибуция.

## Quality gate

Модель не допускается к production, пока не зафиксированы назначение, запрещённые сценарии, данные, метрики по релевантным группам, ограничения, риски, human oversight, SLO, rollback и unit economics.
