# Следующие действия

Статусы: `PLANNED → IN_PROGRESS → REVIEW → VERIFIED → DONE`, отдельно `BLOCKED`.

| Приоритет | ID | Действие | Контур | Выход | Gate | Статус |
|---:|---|---|---|---|---|---|
| 1 | L01-NEXT-001 | Проверить точную формулировку ДЗ | OTUS | submission checklist | OTUS-COVERAGE | IN_PROGRESS |
| 2 | L01-NEXT-002 | Сформировать чистый пакет сдачи | OTUS | README + БФТ + ссылки | OTUS-SUBMIT | PLANNED |
| 3 | L01-NEXT-003 | Утвердить границу Б24/1С | FATHER | ADR-001 | L01-GATE-SCOPE | BLOCKED |
| 4 | L01-NEXT-004 | Провести legal/security review | FATHER | матрица оснований и данных | L01-GATE-LEGAL | BLOCKED |
| 5 | L01-NEXT-005 | Получить схему телефонии | FATHER | PBX/SIP PoC | L01-GATE-PBX | BLOCKED |
| 6 | L01-NEXT-006 | Построить C4 Context | FATHER | context diagram | ARCH-CONTEXT | PLANNED |
| 7 | L01-NEXT-007 | Построить C4 Container | FATHER | container diagram | ARCH-CONTAINER | PLANNED |
| 8 | L01-NEXT-008 | Построить pre-flight sequence | FATHER | sequence diagram | TRACE-BR03 | PLANNED |
| 9 | L01-NEXT-009 | Построить dialog state machine | FATHER | state diagram | DIALOG-COVERAGE | PLANNED |
| 10 | L01-NEXT-010 | Рассчитать нагрузку и SLA | FATHER | load model | PERF-SLA | PLANNED |
| 11 | L01-NEXT-011 | Выполнить 24 теста | FATHER | test report | L01-GATE-TRACE | PLANNED |
| 12 | L01-NEXT-012 | Передать входы в урок 2 | BOTH | оценка, этапы, смета | L01-EXIT | PLANNED |

## Ближайшая контрольная точка

Урок 1 считается завершённым, когда:

- пакет OTUS соответствует формулировке задания;
- расширенный проект FATHER имеет трассировку требований;
- три блокирующих gate закрыты либо явно приняты владельцем риска;
- подготовлены схемы, ADR и тестовый отчёт;
- сформировано решение GO / CONDITIONAL GO / NO-GO.
