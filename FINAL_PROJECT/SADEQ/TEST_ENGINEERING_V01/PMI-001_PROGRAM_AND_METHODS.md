# ПМИ-001 — Программа и методика испытаний программного комплекса SADEQ UAA / P0
**Обозначение:** SADEQ-PMI-P0-001 · **Редакция:** 0.1 · **Дата:** 28.11.2026
**Статус:** ПРОЕКТ, НЕ УТВЕРЖДЕНО · **Фактические результаты:** NOT_RUN по данной ПМИ
**Заказчик:** TBD · **Разработчик:** FATHER/SADEQ R&D · **Испытатель:** TBD · **Независимый экзаменатор:** POLYGON role (not yet instantiated).

## 0. Общие положения и назначение
Настоящая программа устанавливает **что именно, где, при каких исходных условиях и по какой проверяемой методике** должно быть испытано, чтобы утверждать выполнение конкретных пунктов ТЗ и FATHER-CSSC-001. Это не паспорт работоспособности API и не сертификат. Основа структуры документа — действующие ГОСТ Р 59795-2021 и ГОСТ 19.301-79, виды испытаний определяются ГОСТ Р 59792-2021. Применимость к конкретному договору устанавливается отдельно. Полный реестр — [ПМИ-000](PMI-000_SOURCES_AND_STATUS.md).

## 1. Объект испытаний
**Наименование:** корпоративный AI-ассистент SADEQ Enterprise Operations Copilot.
**Комплектность P0:** B01 API+Identity, B02 Object/Event Core, B03 Knowledge/RAG, B04 bounded Agent, B05 independent UAG/approval/action, B07 POLYGON, B08 Operations, offline local inference and synthetic mock ITSM.
**Модификация и идентичность:** candidate git commit SHA, manifest/schema/model/policy/container/source digests, environment fingerprint — записывать в поле протокола **до** испытаний; незаданные параметры блокируют квалификацию.
**Назначение:** подготовка обоснованной помощи оператору обработки тестовых корпоративных заявок.
**Границы:** исключительно synthetic tenant A/B, mock ITSM; без продуктивных серверов, реальных ПДн, внешних LLM API или прав на опасные операции.

## 2. Цели и задачи испытаний
- Подтвердить соответствие заявленным FR-NEW-01…14 для P0 в пределах лабораторной среды.
- Проверить обязательные запреты FATHER-CSSC-001 SI-01…SI-18 на заданном перечне угроз.
- Доказать одно бизнес-событие на повтор, однозначную идентичность, отсутствие обхода ACL и запрещённых tool calls.
- Проверить что proposed action требует реального согласования, и что успех подтверждается **authoritative read-back**, а не самим ответом LLM или HTTP 200.
- Измерить latency, memory/VRAM, токены, throughput и реальные ресурсы при согласованной нагрузке; **численные пороги TBD до acceptance test**, не назначать после измерения.

## 3. Основания и предъявляемая документация
Входящие документы: ТЗ-003, IDEA+0.3, HLD ЭП-003, TP-001…005, JSON Schemas, API policy matrix, Threat Register, synthetic test corpus manifest, model manifest, sbom, code commit, инструкции установки/эксплуатации, протоколы предварительных испытаний; отсутствующие документы обозначать `BLOCKED`.
Источники: [ПМИ-000](PMI-000_SOURCES_AND_STATUS.md). Ссылки на отдельные требования приведены в [ПМИ-003](PMI-003_TEST_TRACEABILITY_REGISTER.md).

## 4. Условия проведения и испытательный стенд
### 4.1 Состав
- **LAB host:** Windows 11 / Python 3.12; CPU, RAM, GPU, версия CUDA, driver, WSL2/Docker записываются из фактического стенда.
- **Services:** FastAPI, PostgreSQL, Qdrant, Ollama, mock ITSM, UAG; LangGraph; при частичном составе тесты отсутствующих узлов `BLOCKED`, а не PASS.
- **Datasets:** MAT-01..11 synthetic rights-cleared, SHA256 corpus and golden cases, DEV/VALIDATION/HELDOUT partition.
- **Identities:** distinct tenant A/B, subject A operator, subject A approver, security reviewer, B01 service identity, B05 tool identity. No demo x-headers for security qualification.
- **Network:** offline/egress-deny profile for full-P0 security exam. Capture network restrictions and permitted endpoints.

### 4.2 Начальные условия
Clean temporary DB with approved migrations; deterministic seeds and fixture manifest; host clock synchronized; mock ITSM state `INC-001=NEW, version=1`; source SOP `SOP-01` approved for tenant A, no tenant B permission; candidate hash fixed; system ready; examiner granted read-only results/evidence access.

### 4.3 Сведения, фиксируемые до запуска
`test_plan_revision; approved_requirement_revision; environment_id; OS; Python; dependency lock; code_commit; container_digest; model_digest; schema_hash; policy_hash; dataset_hash; source_registry_hash; seeded_state_hash; examiner; UTC timestamp; test_run_id`.

## 5. Средства испытаний
- HTTP test client / pytest for contract and system tests, JsonSchema/Pydantic for data shapes, test PostgreSQL for transactional behavior.
- Synthetic mock ITSM supporting prescribed idempotency + fault injection + authoritative GET; HTTP/API tracer with redaction.
- Auth test provider for verified tokens/claims and rejected issuer/audience/role.
- Runtime metrics, DB snapshots, request/response digests and signed candidate manifest.
- Independent POLYGON suite for hidden holdout and regression; exact tools, pinned dependencies and approvals TBD.

## 6. Программа испытаний — последовательность допусков
| Этап | Объект | Основание | Тесты | Условие перехода |
|---|---|---|---|---|
| E00 | Предъявленная документация | Секции 1–5, PRJ-01/02 | DOC-001.. | input complete, edition frozen |
| E01 | Контракты и identity B01 | FR-NEW-01/02, SI-01/02/14 | API-001..008 | no critical auth/schema bypass |
| E02 | Object/Event B02 | FR-NEW-03/04, SI-02/12 | EVT-001..007 | no duplicate effect / cross-tenant merge |
| E03 | Sources/RAG B03 | FR-NEW-05/06, SI-03/07 | RAG-001.. | citation provenance and ACL on all test cases |
| E04 | Reasoning B04 | FR-NEW-07/08 | AGT-001.. | bounded and typed proposal / ABSTAIN |
| E05 | UAG/ITSM B05 | FR-NEW-09/10/11, SI-05/09/10/11/12 | ACT-001.. | approval-bound action + readback |
| E06 | Security full stack | FR-NEW-13/14, SI-01..18 | SEC-001.. | no critical unauthorized actions/leaks in defined suite |
| E07 | Resilience/performance | FR-NEW-12, quality targets | PERF-001.. | reproducible metrics and agreed targets |
| E08 | Independent POLYGON | FR-NEW-13, SI-18 | QUAL-001.. | independent evidence, hash match |
| E09 | Human release decision | TZ-003 §2.3 | REL-001 | decision signed / BLOCKED |

**Partial execution:** E01 schema-only may be run on present code, but gives no right to report E06/E08 success.

## 7. Методики испытаний
Each test shall be approved as a standalone passport in the structure of [ПМИ-004](PMI-004_TEST_CASE_TEMPLATE.md). A concrete filled passport for tenant isolation and header spoofing is [ПМИ-002](PMI-002_CASE_API001_TENANT_ISOLATION.md).
For each test, mandate:
1. `Requirement ID → source clause → invariant → threat → test purpose`.
2. Context and exact environment, initial authoritative state and fixture/hash.
3. Block/component sequence diagram plus negative trust boundary.
4. Setup, execution stimulus, expected API/DB/tool/audit/postcondition, observable counters.
5. Specific PASS/FAIL/BLOCKED conditions and cleanup/rollback.
6. Raw evidence path/hash, independent observations, result and issue for deviation.
In case of disagreement, **the approved test passport and immutable contract precede code output**. Changing the expected result requires formally reviewed change, not silent adaptation.

## 8. Методы обработки результатов
- `PASS` only if **all** defined assertions pass with evidence; `FAIL` if any assertion violated; `BLOCKED` if prerequisite or environment is absent; `NOT_RUN` if no test executed; `INCONCLUSIVE` if evidence is insufficient. Distinguish this from outcome statuses `DENY, REJECT, ABSTAIN` of system.
- A denial can be a **PASS** for a negative test only when exact expected denial, no side effects and audit evidence are proved.
- Security hard gate: any demonstrated cross-tenant leak, permission/approval bypass or unauthorized tool effect → E06 FAIL and release BLOCKED.
- Unexpected external side effect or failed test must be recorded; rerun must preserve prior report and explain correction.
- **Acceptance criteria thresholds for performance/AI quality must be agreed before E07/E08**, no post-hoc thresholds.

## 9. Оформление протокола и отклонений
Protocol per run: registration info, candidate manifest, examiner signature, environment, results per TEST-ID, raw logs/redactions, DB pre/post state, mock ITSM GET record, denied action counters, SHA256 manifests, deviations/defects, remediation links, judgment.
Suggested [protocol template](PMI-005_TEST_PROTOCOL_TEMPLATE.md). CI artifacts are technical evidence; they are not official acceptance acts.

## 10. Ответственность, безопасность, защита данных
- Developer: implementation and self-test; may propose correction but not certify independently.
- Test lead: freeze program, test data and expected results, assign examiner.
- Security owner: approve policy and high-risk negative tests; no production secrets in test.
- Independent examiner: POLYGON rerun and evidence verification; cannot alter candidate or heldout.
- Customer/release authority: approves final release; **not assigned in current research project**.
- Fault injection only in isolated synthetic services; any sign of production exposure → stop tests and investigate.

## 11. Условия завершения
Preliminary ready when all **applicable** E00–E07 completed and documented; independent qualification E08 and human E09 required to make P0 release claim. `NOT_RUN`/missing mandatory P0 evidence is **NO-GO**; exception process can only waive optional nonsecurity tests with named approver and written risk acceptance, not fabricate PASS.

### Лист согласования
Developer: `UNSIGNED` · System owner: `TBD` · Security owner: `TBD` · Test lead: `TBD` · Independent examiner: `TBD` · Customer: `TBD`.
