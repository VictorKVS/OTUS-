# TP-005 / FATHER-CSSC-001 — Contract-Strict Security Contract Standard
**SADEQ / FATHER. Версия 0.1. Дата: 28.11.2026. Статус: PROPOSED / REVIEW_REQUIRED / TESTS_NOT_RUN.**

## 0. Неприкосновенное правило проекта
Контракт — **не только OpenAPI + JSON Schema**, и не только описание того, что отправитель должен передать. Каждый контракт описывает **взаимные обязательства, явно запрещённые действия, разрешённые переходы, права, входные и выходные ограничения, инварианты, последствия отказов и проверяемые evidence**. Контракт существует между *доверенными идентифицированными субъектами* и не может делегировать полномочия за пределы заранее утверждённой capability boundary.

**Слои:** BUSINESS (исход и последствия), COMPONENT (кто владеет состоянием), DATA (типы, классификация, provenance), SECURITY (идентичность, права, запреты, threats), EXECUTION (таймаут, retry, транзакция), QUALIFICATION (негативные тесты, evidence). Один контракт получает шесть согласованных паспортов или единую спецификацию с шестью разделами.

## 1. 22 обязательных поля паспорта любого FLOW/API/TOOL
| # | Поле | Что обязано быть зафиксировано |
|---|---|---|
| C01 | Identity/version/owner | `FLOW-ID`, `API-ID`, `ALG-ID`, semver, approving owner |
| C02 | Purpose | единственная разрешённая бизнес-цель; out-of-scope |
| C03 | Sender identity | проверенный отправитель, аутентификация и допустимые workload identities |
| C04 | Receiver / allowed routing | ровно допустимый получатель, запрет произвольного маршрута |
| C05 | Subject / delegation | в чьих интересах вызов, источник tenant/principal; правила делегирования |
| C06 | Resource | объект/tenant/data-classification/состояние, над которым разрешено действие |
| C07 | Precondition | проверяемые предпосылки и версия объекта |
| C08 | Request Schema | `additionalProperties:false` на всех объектах, max length/depth/items, exact enums, media type |
| C09 | Response Schema | закрытый ответ, whitelist выдаваемых полей, данные на уровне property-level ACL |
| C10 | Invariants | что нельзя менять и какие свойства сохраняются всегда |
| C11 | Postcondition | авторитетный источник результата и независимая проверка |
| C12 | Explicit DENY | запрещённые операции / поля / маршруты / избыточные права / implicit defaults |
| C13 | Decision matrix | allow / deny / approval required / abstain / review |
| C14 | Error taxonomy | typed errors, 4xx/5xx, redaction, no internal stack or secrets |
| C15 | State & transaction | атомарность, ownership, optimistic lock, outbox, replay |
| C16 | Idempotency / retries | уникальность, request digest, TTL, bounded retry, reconcile unknown |
| C17 | Availability / budgets | rate limit, payload size, timeout, concurrency/tokens/CPU/GPU quota, backpressure |
| C18 | Cryptography & transport | TLS/mTLS where needed, token audience, expiry, signing, key/rotation assumptions |
| C19 | Data governance | origin, retention, deletion, no secrets in trace, approved ingestion |
| C20 | Observability | trace_id, auth decision ID, redacted log, severity, metrics |
| C21 | Threat mapping | OWASP API category, STRIDE, threat and mitigation IDs |
| C22 | Acceptance & evidence | positive, negative, property/fuzz/concurrency, reviewer, artifact hash, NOT_RUN until execution |

**Contract freeze blocked** if any mandatory field is `TBD` on production trust boundary, or if sender/receiver/subject/resource ownership remain ambiguous.

## 2. Mandatory security invariants SEC-INV-01...18
| ID | MUST / MUST NOT | Negative evidence |
|---|---|---|
| SI-01 | deny by default; authenticate **every** untrusted request | unauthenticated request has no protected side effects |
| SI-02 | tenant and principal come from verified session, not payload/header spoof | cross-tenant forged ID denied |
| SI-03 | check object-level authorization per request, not only at list endpoint | IDOR / BOLA 403 or masked 404 |
| SI-04 | check each field for read/write disclosure, no mass assignment | `is_admin`, `owner`, `tenant_id` forbidden |
| SI-05 | independently check function/tool/operation-level authorization | call unauthorized endpoint/tool denied |
| SI-06 | authorize **service** and **user-to-resource** separately | authenticated service cannot act on arbitrary user object |
| SI-07 | LLM outputs are untrusted: cannot modify security policy or obtain credentials | injection request has no privileged effect |
| SI-08 | allowed tool must be enumerated, fixed destination; no arbitrary URL/SSRF | tool host replacement denied |
| SI-09 | proposal is immutable, action hash binds target/state/args/expiry, approval is authenticated and expiring | hash mismatch / stale approval denied |
| SI-10 | recheck policy and exact state version **immediately before tool execution** | TOCTOU concurrent change denied |
| SI-11 | never claim success on API 200 without authoritative postcondition | unchanged state ⇒ MISMATCH |
| SI-12 | ambiguous timeout ⇒ EXECUTION_UNKNOWN and reconcile, never blind replay | duplicate mutation not accepted |
| SI-13 | use bounded request, token, concurrency and GPU quotas | oversized/flood ⇒ 413/429/503 no crash |
| SI-14 | validate content-type, actual parser, max nesting, UTF8, duplicate JSON keys; reject ambiguous requests | polyglot/duplicate keys denied |
| SI-15 | protect transport and tokens: audience/issuer/expiration/key rotation; PKCE for appropriate browser clients; appropriate sender constraints | expired/wrong-aud token denied |
| SI-16 | no PII/secrets/passwords/LLM prompt internals in logs/error responses | redaction tests |
| SI-17 | no unsecured egress or unapproved external inference in offline profile | deny-egress evidence |
| SI-18 | independent POLYGON heldout and human signoff required; qualification invalidated by relevant change | changed model/policy cannot reuse old seal |

**Property-level permission is *not* accomplished merely by `additionalProperties:false`**. For example, a schema may allow `status`, yet a specific user is forbidden to change it; enforced policy per resource and field is still mandatory.

## 3. Contract example — FLOW-06/07/08
| Side | MUST | MUST NOT |
|---|---|---|
| B04 proposer | produce structured `ActionProposalV1`, evidence refs, object/version, postcondition | invoke tool, provide credentials, assert its own approval |
| B05 UAG | authenticate service+subject, verify tenant/resource/function/field, assess risk, obtain human approval, recheck state | use LLM answer as authorization, accept stale or changed proposal |
| Approver | review immutable exact action; authorize only delegated scope and within TTL | approve foreign tenant, change object without new approval |
| Tool adapter | accept only UAG-scoped call, fixed endpoint/status, idempotency token, returns receipt | accept raw agent messages, call arbitrary host, write directly to DB |
| ALG-12 verifier | read authoritative ITSM record, compare expected state, report evidence | treat HTTP 200, model assertion or unchanged state as business success |
| B07 POLYGON | test exact version with hidden suite and separate privileges | mutate candidate or self-authorize release |

### Decision table (concept)
| Auth | Tenant/Object/Field | Qualified version | Human decision | State unchanged | Outcome |
|---|---|---|---|---|---|
| no | any | any | any | any | DENY |
| yes | denied | any | any | any | DENY |
| yes | allowed | invalid/expired | any | any | DENY |
| yes | allowed | valid | missing | yes | APPROVAL_REQUIRED (for action with required HITL) |
| yes | allowed | valid | approved but stale | no | STALE / DENY |
| yes | allowed | valid | approved and bound | yes | EXECUTE, then VERIFY |
Only the last line may invoke the allowlisted tool. This table requires formal policy owner approval before code.

## 4. OWASP mapping and tests
| OWASP API 2023 | Risk | SADEQ test |
|---|---|---|
| API1 BOLA | foreign object ID | T-SEC-API01 object isolation |
| API2 Broken Authentication | invalid token/identity | T-SEC-API02 no acceptance |
| API3 Broken Object Property Level Authorization | mass assignment, overexposed responses | T-SEC-API03 forbidden field/response |
| API4 Unrestricted Resource Consumption | huge body, high cost, GPU exhaustion | T-SEC-API04 quotas/timeouts |
| API5 Broken Function Level Authorization | unauthorized function/tool | T-SEC-API05 blocked tool |
| API6 Unrestricted Access to Sensitive Business Flows | high-rate approval/create operations | T-SEC-API06 workflow abuse |
| API7 SSRF | arbitrary HTTP/URL from doc/tool | T-SEC-API07 fixed destinations |
| API8 Security Misconfiguration | debug logs, CORS, TLS, headers | T-SEC-API08 config |
| API9 Improper Inventory Management | shadow endpoints, unversioned/legacy APIs | T-SEC-API09 inventory |
| API10 Unsafe Consumption of APIs | untrusted backend/third-party results | T-SEC-API10 validate receipt + verify actual state |

Plus LLM-specific prompt injection, indirect injection from SOP, tool-output poisoning, RAG ACL evasion and model update regression in separate AI threat matrix.

## 5. Book-grounded method vs official standards
**Previously studied book:** Justin Richer & Antonio Sanso, *OAuth 2 in Action*, Ch.1 and Ch.13: OAuth is authorization delegation; it is not itself authentication, and token/scope semantics are chosen by the API/resource owner. These points were checked against the user's uploaded book. **Do not copy the book's historical browser implicit-flow advice** into a modern P0 design without reviewing the newer OAuth BCP.

**Previously cited engineering foundation:** Gough / Bryant / Auburn, *Mastering API Architecture* — API boundary, interface lifecycle, versioning and contract-testing *as described in SADEQ prior design notes*. **Exact book passage not verified here**; add bibliographic chapter/page IDs after direct inspection before claiming this book as source of individual MUST clauses.

**Binding primary standards:**
- [OWASP API Security Top 10:2023](https://api-security.owasp.org/editions/2023/en/0x11-t10/) — threat catalogue (not a certification).
- [NIST SP 800-228-upd1, March 2026](https://csrc.nist.gov/pubs/sp/800/228/upd1/final) — protection of cloud-native APIs, service and resource authorization; apply proportionately to on-prem.
- [OAuth 2.0 Security BCP, RFC 9700 (January 2025)](https://www.rfc-editor.org/rfc/rfc9700.html) — modern access token/grant recommendations.
- [OAuth 2.0 for Browser-Based Applications RFC 10017 (August 2026)](https://www.rfc-editor.org/rfc/rfc10017.html) — browser client practices; authorization code with PKCE and/or BFF design, no legacy implicit grant.
- [OpenAPI 3.1.2](https://spec.openapis.org/oas/v3.1.html) — spec and securityScheme metadata, **not runtime enforcement**.
- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12) — structural validation, **not identity or ACL policy**.
The normative language MUST/MUST NOT here is **an internal proposed project standard**, not a verbatim quotation from any reference.

## 6. Engineering workflow / review stop-points
1. Register the SRC reference and business requirement.
2. Define API/component/data *positive behavior* and all explicitly prohibited operations.
3. Model trust boundary, object- and field-level ACL, tool allowlist.
4. Freeze schemas and semantic invariants, state machine and error/recovery.
5. Threat model OWASP, STRIDE and agent-specific threats; prioritize abuse cases.
6. Write negative tests **before** implementation, and at least one test for every "MUST NOT".
7. Implement independent deterministic checks and scoped credentials, no free-form model execution.
8. Run unit/contract/integration/fuzz/property/security/load/offline tests; collect evidence hash.
9. Separate reviewer approves changed contracts; POLYGON requalifies exact image/model/policy/data version.
10. Code only deployable with human-owned release decision and auditable rollback.

## 7. Immediate gaps in TP-001: blocking, explicit
- Existing schemas cover 4 request types only; **no response schema**, FLOW-08/09, policy decision schema, content classification, rate budget, detailed auth token requirement, security error model.
- `InboundIncidentV1` missing payload-level anti-mass-assignment security *execution* (the shape alone prevents `tenant_id` but not downstream ORM auto-bind).
- `ActionProposalV1` semantic mismatch `arguments.new_status != expected_postcondition.status` currently passes JSON Schema and must be denied by code or schema cross-field mechanism.
- Need cross-language canonical JSON format or single-runtime hash contract and replay-safe request signature.
- Current `pytest` is design-only and was **not run in user environment**; no evidence should be marked PASS.
- Add `ResponseEnvelopeV1`, `PolicyDecisionV1`, `AuthorizedToolCallV1`, `AuthoritativeStateV1`, an OpenAPI spec with security requirements, contract conformance harness, and a matching negative-case matrix.

## 8. Release rule
**Contract** status values: `DRAFT → REVIEW_REQUIRED → APPROVED_FOR_TEST → IMPLEMENTED → VERIFIED → QUALIFIED`. Only human reviewer can promote; tests cannot set their own acceptance or conceal unmet controls. Unreviewed additional fields or changed API permission scopes invalidate previous qualification.
