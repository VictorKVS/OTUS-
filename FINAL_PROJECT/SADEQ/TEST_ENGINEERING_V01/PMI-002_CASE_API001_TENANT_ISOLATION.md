# ПМИ-002 — Методика API-001: доверенная идентичность и межорганизационная изоляция
**TEST-ID:** `T-SEC-API01` / `API-001` · **Revision:** 0.1 · **Category:** security, negative, functional.
**Status:** TEST SPECIFICATION DRAFT / NOT_EXECUTED under this PМИ.

## 1. Постановка задачи
**Контекст:** SADEQ получает заявки сотрудников в закрытой корпоративной среде. В системе существуют `tenant-a` и `tenant-b` с одинаковым внешним ID `INC-001`. Пользователь A пытается получить или изменить объект B путём подмены идентификатора в заголовке либо URL. При этом сервис не должен ошибочно принять параметр запроса за доверенную identity.
**Цель:** доказать, что только проверенный сервером authenticated subject + recipient + object + tenant policy определяют права и что запрос к чужому объекту не выдаёт данных и не создаёт действий.
**Бизнес-значение:** предотвращение раскрытия корпоративных обращений другой организации/подразделения и несанкционированного изменения заявок.
**За пределами:** криптостойкость реального корпоративного IdP, продуктивная ITSM и физическая защита инфраструктуры.

## 2. Основания и источники
| ID | Опора | Применимость |
|---|---|---|
| R-01 | ТЗ-003 4.1.3, FR-NEW-02, FR-NEW-09 | проверенная личность, tenant binding, denied cross-tenant |
| R-02 | FATHER-CSSC-001 C03/C05/C06/C12, SI-01/02/03/04/06 | trusted auth, object/field authorization, explicit DENY |
| R-03 | OWASP API Security Top 10:2023 API1 BOLA; API2 Broken Authentication; API3 Property-Level Authorization | abuse case design |
| R-04 | ГОСТ Р 59795-2021 §5.13 | структура программы и методики; точный применимый подпункт проверить при formal approval |
| R-05 | ГОСТ 19.301-79, разделы программы/методики | форма испытания программного модуля |
| R-06 | [InboundIncidentV1](../TECHNICAL_PROJECT_V01/contracts/InboundIncidentV1.schema.json) | внешнее тело не содержит tenant/role |
| R-07 | [TP-001 contracts](../TECHNICAL_PROJECT_V01/TP-001_INTERFACE_CONTRACTS.md) | identity from verified middleware |

## 3. Объект и метод
**Object under test:** B01 incoming API + B05 authorization; verified identity provider and B02 tenant-indexed object store. Current prototype has X-Demo identity headers and therefore **does not meet the prerequisite for actual security PASS**; an implementation check against it may record FAIL only.
**Method:** black-box API attempt and white-box side-effect reconciliation with independent examiner. Severity: CRITICAL if unauthorized read/write.

## 4. Предусловия
- Lab isolated; no internet or real enterprise API.
- Test identity provider issues verified subject `user-a` with tenant `tenant-a`, role `operator`; valid subject `user-b` for tenant-b; separate approver.
- B02 store has objects `tenant-a/INC-001` and `tenant-b/INC-001` with **different synthetic contents**, separate versions, distinct DB object IDs.
- Verify that auth middleware rejects unsigned/expired/wrong-audience credentials before calling B02; no plain `X-Demo-Tenant` trust.
- EVIDENCE has redaction policy; test harness captures trace ID, DB state before/after and tool-call counter.
- Dataset SHA, policy version and exact commit/hash pinned; if unavailable → `BLOCKED`.

## 5. Схема маршрута и границ доверия
[Source sequence diagram](diagrams/PMI_API001_SEQUENCE.mmd) and design in [HLD](../SKETCH_PROJECT_V01/EP-003_HLD_BOUNDARIES.md).
**Boundary A:** HTTP untrusted request → B01 identity verification.
**Boundary B:** B01 trusted `AuthContext` → B02 per-object read.
**Boundary C:** B04 proposal → B05 policy → external adapter; this test must show NO call when unauthorized.
**Forbidden:** use attacker-supplied `tenant_id` from JSON/header/query, identity from LLM output, cross-tenant cache hit, privileged tool call.

## 6. Исходные данные
| ID | Data | Owner / source | Expected |
|---|---|---|---|
| D-01 | valid signed token user-a/tenant-a | synthetic IdP test issuer | authenticated |
| D-02 | absent credential | API client | authentication failure |
| D-03 | forged unsigned `X-Demo-Tenant: tenant-b` | attacker-controlled header | ignored / rejected |
| D-04 | tenant-b/INC-001 | synthetic B02 fixture | forbidden to user-a |
| D-05 | tenant-a/INC-001 | synthetic B02 fixture | allowed if role permits |
| D-06 | `{"tenant_id":"tenant-b"}` in request body | attacker-controlled payload | schema REJECT |
All data are synthetic and must be in a versioned, hashed test corpus.

## 7. Программа одного испытания и ожидаемые состояния
| Step | Procedure | Expected HTTP / policy | Expected system state |
|---|---|---|---|
| 0 | snapshot tenant A+B object hashes and mock ITSM call count | control snapshot recorded | unchanged |
| 1 | authorized user-a fetches tenant-a/INC-001 | 200 with **only approved response fields** | no mutation |
| 2 | user-a tries tenant-b/INC-001 via path/query | 403 or masked 404 according to approved API spec | no response data from tenant-b; no mutation |
| 3 | send `X-Demo-Tenant: tenant-b` with token user-a | ignored/rejected; still tenant-a authority | no tenant-b data |
| 4 | submit incoming incident with `tenant_id` or `role=admin` in body | 422 schema reject | no new event/receipt/tool action |
| 5 | send request unauthenticated and with expired/wrong audience token | 401 | no protected side effect |
| 6 | try approval action for B using A operator | 403/404 | zero tool calls, no approval record |
| 7 | compare DB A/B object hashes, event counts, audit trace and tool log | hashes unchanged for forbidden operations | no cross-tenant leak |
| 8 | verify audit contains denied decision but **not** secret or tenant-b payload | redacted log | evidence trace record |

Allowed 403 vs 404 must be frozen into **one** endpoint-specific contract before accepting result; no per-run interpretation.

## 8. Критерии оценки
**PASS**: authorized A path works; each negative request returns exact contract status; no forbidden fields/snippets, no B object mutation, no illicit tool calls, trace of denial exists; all evidence bound to version/hash. **FAIL:** unauthorized tenant-b data read, changed B object or unexpected tool call, spoofed identity accepted. **BLOCKED:** no valid signed identity environment, no policy owner or no authoritative state snapshot. **INCONCLUSIVE:** missing log/DB evidence; cannot claim PASS.

## 9. Нагрузка, восстановление и повторяемость
For security baseline run 1 case per subtest; concurrency and BOLA enumeration fuzzing are separate stress tests. Restore DB from seeded snapshot and re-run under unchanged candidate hash; report diff of denial decisions. Any testcase modification after result changes test revision and requires rerun.

## 10. Оформление результатов
No actual results yet. Complete [протокол](PMI-005_TEST_PROTOCOL_TEMPLATE.md) with environment, source/dataset SHA256, before/after DB hashes, sample redacted HTTP, policy audit IDs, signature, failure/issue ID, and recommendation. No auto-generated PASS without independent review.
