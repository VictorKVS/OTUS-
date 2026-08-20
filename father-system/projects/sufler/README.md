# FATHER Project: SUFLER

**ID:** `FATHER-PROJECT-SUFLER`  
**Учебный источник:** `OTUS-L01-HW-001`  
**Назначение:** полный профессиональный цикл проектирования голосового AI-ассистента.

## Граница

Этот каталог не является домашней работой для непосредственной сдачи OTUS. Он использует учебный кейс как тренировочный проект для развития доказательной памяти и навыков AI-архитектора.

## Производственный маршрут

| Этап | Каталог | Выход | Статус |
|---|---|---|---|
| 01 | `01-intake/` | цели, контекст, стейкхолдеры | IN_PROGRESS |
| 02 | `02-requirements/` | BR/FR/NFR и трассировка | REVIEW |
| 03 | `03-risks/` | риски и противоречия | REVIEW |
| 04 | `04-legal-security/` | заключения ИБ и юриста | BLOCKED |
| 05 | `05-economics/` | TCO, оценка, резерв | PLANNED |
| 06 | `06-architecture/` | C4, sequence, state machine | PLANNED |
| 07 | `07-decisions/` | ADR | PLANNED |
| 08 | `08-tests/` | 24+ проверочных сценария | PLANNED |
| 09 | `09-delivery/` | GO / CONDITIONAL GO / NO-GO | PLANNED |

## Доказательный статус

Документ заявлен как «Готов к проектированию». По результатам проверки статус: **CONDITIONAL GO**.

Блокеры:

1. граница интеграции Б24/1С;
2. правовые основания звонков, SMS, записи и транскрибации;
3. совместимость Asterisk/SIP REFER.

## Связанные данные

- `../../../knowledge/lesson-01/homework-sufler.graph.json`
- `../../../knowledge/lesson-01/homework-sufler.assessment.json`
