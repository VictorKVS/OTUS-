# ТП-004 — Контрактное тестирование / программа подготовительных проверок
**Статус:** TEST_DESIGN / NOT_RUN. Данный документ — инженерные проверки, не заменяет утверждённую ПМИ ГОСТ 34.603 или ГОСТ 19.301.

## 1. Минимальный исполняемый контрактный тест
`python -m pip install "jsonschema[format]>=4.21,<5" pytest` (пин exact version + hashes обязательны перед qualification), затем из корня этого пакета `python -m pytest -q tests/test_json_contracts.py`.
**Команда и файл подготовлены, выполнение теста в пользовательской лаборатории пока не подтверждено.**

## 2. Test catalog and expected results
| ID | Input | Expected | Req |
|---|---|---|---|
| T-SCHEMA-001 | `inc_001_valid.json` | `InboundIncidentV1` VALID | FR-NEW-01/02 |
| T-SCHEMA-002 | nested `internal_role` | INVALID: additionalProperties | FR-NEW-02 |
| T-SCHEMA-003 | supplied `tenant_id` | INVALID: additionalProperties | FR-NEW-02/09 |
| T-SCHEMA-004 | missing `source_system` | INVALID | FR-NEW-02 |
| T-SCHEMA-005 | `priority=P0` | INVALID | FR-NEW-02 |
| T-SCHEMA-006 | wrong `observed_at` format | INVALID with format checker | FR-NEW-02 |
| T-SCHEMA-007 | extraneous nested action argument | INVALID | FR-NEW-08 |
| T-SCHEMA-008 | mismatched action/postcondition | **JSON shape may pass; semantic validator must reject** | FR-NEW-08/09 |
| T-AUTH-001 | spoofed tenant principal | DENY at trusted auth boundary, not merely JSON | FR-NEW-09 |
| T-OBJ-001..007 | duplicate/replay | deterministic DB uniqueness and replay | FR-NEW-03/04 |
| T-ACT-001..008 | permissions/unknown tool/stale/timeout | deny or reconciliation; no silent side effect | FR-NEW-09/10/11 |
| T-RAG-001.. | malicious source/foreign source | citation+ACL+supported answer | FR-NEW-05/06 |
| T-POLYGON-001.. | independent heldout and release | pass/fail report for exact version | FR-NEW-13 |

## 3. Evidence obligations
Record test code commit, dataset SHA, schema files SHA, dependencies, Python version, validator version, OS, test run stdout, expected/actual, reviewer, timestamp; attach generated report only after actual execution.
**No PASS assertion for current set.** No claims about offline egress/K8s without actual runtime.

## 4. Next development gate
P0 contract freeze demands runnable validator, actual tests of all four schemas, strict HTTP decoder and verified auth-context, then transactional event store + mock ITSM, then end-to-end and POLYGON.
