# ЭП-003 — Системная архитектура / HLD
**Статус:** DRAFT / REVIEW REQUIRED; настоящий C4 исходник и deployment design потребуют дополнительной формальной проверки.

## 1. Модель взаимодействий
Внутри одного корпоративного доверенного периметра действуют разные **зоны полномочий**, которые нельзя смешивать логически или по credential access. Физическое разделение на сервисы/Pod уточняется после теста; C4 logical container ≠ Kubernetes container.
[Текущая обзорная C4-схема](../IDEA_PLUS_REBASELINE_V03/diagrams/VIS-03_C4_CONTEXT_CONTAINER.svg).

## 2. Участники и внешние системы
Actors: operator, approver, service owner, data owner, security reviewer, SOC/platform engineer, independent POLYGON examiner.
Upstream: approved SOP repository + synthetic ticket source, local identity provider. Downstream: mock ITSM through strictly scoped adapter. Internal: PostgreSQL/event store, Qdrant, Ollama, metrics; P1 Neo4j/GraphRAG, K8s.

## 3. B01–B08 — ownership и жизненный цикл
| Блок | Главная зона ответственности | Первая поставка | Нет права |
|---|---|---|---|
| B01 Integration/Security Edge | identity, closed schema, trusted transport | P0 | принимать LLM как identity source |
| B02 Objects/Events | dedupe, canonical object, append-only event, state reducer | P0 | подменять внешний authoritative ITSM |
| B03 Knowledge/Evidence | approved document import, ACL filters, source refs, RAG | P0 (Neo4j P1) | брать чужой tenant источник |
| B04 AI/Orchestration | bounded agent workflow, hypotheses, typed proposal | P0 | выдавать разрешение tool |
| B05 UAG/Action | independent policy, scoped approval, exactly-once **business-effect goal**, verify | P0 | исполнять без проверенного права |
| B06 Factory | new profiles/agent manifests; narrow config registry for P0 | thin P0 registry, full P2 | принимать своё изменение в production |
| B07 POLYGON | independent tests, signed evidence proposal | P0 | править candidate |
| B08 Operations | deploy, logs, metrics, provenance, backup/rollback | P0 compose; P1 K8s | назначать себе права на выпуск |

**Важное уточнение:** exactly-once delivery между разными системами не гарантируется; используем идемпотентный бизнес-эффект и сверку, с обработкой `EXECUTION_UNKNOWN`.

## 4. Минимальные логические информационные контракты
| FLOW | Source → Target | Typed payload | Acceptance boundary |
|---|---|---|---|
| FLOW-01 | Source → B01 | `InboundIncidentV1` + trusted identity context | reject unknown fields, classify, rate-limit |
| FLOW-02 | B01 → B02 | `ValidatedObservationV1` | tenant from auth, provenance |
| FLOW-03 | B02 → B04 | `ObjectStateRefV1` | immutable ref/state version |
| FLOW-04 | B04 → B03 | `AuthorizedEvidenceQueryV1` | ACL enforced inside knowledge boundary |
| FLOW-05 | B03 → B04 | `EvidenceBundleV1` | citations/source digest, no secret material |
| FLOW-06 | B04 → B05 | `ActionProposalV1` | no credentials or arbitrary tool args |
| FLOW-07 | B05 → Approver | `ApprovalRequestV1` | action hash/state/TTL |
| FLOW-08 | B05 → Mock ITSM | `AuthorizedToolCallV1` | scoped token/idempotency |
| FLOW-09 | ITSM → B05 | `AuthoritativeObjectStateV1` | compare postconditions |
| FLOW-10 | All → B08/B07 | `RedactedTraceV1`, `EvidenceManifestV1` | anti-tamper, no sensitive logs |

The above are **design names**, not published schemas. LLD must define fields, nested `additionalProperties:false`, examples, OpenAPI refs, error matrices and unit/contract tests. Existing open payload in older API v0.1 is **not qualified**.

## 5. Independent security plane
- Policy logic is deterministic and outside LLM.
- No global tenant filter applied only in UI: ACL must be enforced at retrieval and graph-index boundaries, tool execution, caches, and audit reads.
- Qualified model version is not a permission to bypass approval for individual actions.
- Candidate cannot edit heldout tests or issue production release; platform operator has no blanket data owner privileges.
- Absent authorization, ambiguous object or stale state → fail closed.

## 6. Data and state
PostgreSQL stores canonical objects/events/receipts, checkpoint references, authorization/audit metadata; Qdrant stores derived index scoped by tenant; source document repository stores approved bytes and hashes; local inference provider holds model manifest/digest. ITSM remains **authoritative owner of ticket outcome** after action; B02 event log is authoritative only for SADEQ's observations and internal state. This avoids conflating system-of-record ownership.

## 7. Design exits
HLD can proceed to LLD when: business scenario and owners assigned or simulated, B01–B08 interfaces agreed, threat model has trust boundaries, API types frozen, acceptable deployment topology evaluated, and all P0 requirements link to a test.

[Pre-existing broader HLD](../PRODUCT_BASELINE_V1/HLD_V01/02_C4_CONTEXT_CONTAINER.md) remains architecture research source; this document refines P0 scoping.