# SADEQ-SDLC-001 — Сквозная программа безопасной разработки (13 фаз)
**Дата:** 2026-11-27 · **Версия:** 1.0 · **Состояние:** PROJECT SPECIFICATION, НЕ ВНЕДРЕНО.  
**Опора:** FATHER Contract-Strict / Algorithm-Bound Data Flow, IDEA+, шесть SEC ролей, UAG, POLYGON, OTUS 1–31, NIST SSDF, OWASP, SLSA и Kubernetes checklist.

## Жёсткий принцип
**Ни один компонент не считается готовым, пока его безопасность, бизнес-результат и работоспособность не доказаны в составе целевого продукта.** Созданный документ/код/тест ≠ реально выполненный и пройденный тест. Перечень угроз: [100 сценариев](TOP_100_THREATS.md).

## Сквозные фазы
| Phase | OTUS / задача | Вход | Обязательные технические работы | Security роль | Что отдаём (evidence) | Gate |
|---|---|---|---|---|---|---|
| S00 — Product mandate | уроки 1–3: пресейл, требования и цена | бизнес-цель, сценарии | область автоматизации; законность данных; жизненный цикл; классификация вреда и запретных действий | SEC-01 | IDEA+, BIA, business capability map, risk owner, user stories, scope decision | G00: нет risk owner / вредной автономии → STOP |
| S01 — Business analysis | 1–3 и 30 | AS-IS, stakeholder map | BPMN AS-IS/TO-BE, UML actor/use case, RACI, DMN допуск, value stream, ROI гипотезы | SEC-01 | BPMN XML, decision table, RACI, initial DFD | G01: нет разрешённого бизнес-процесса → STOP |
| S02 — Architecture and threat modeling | 4–5, 8–10, 14 | approved goals | C4 L1–L4, trust boundaries, STRIDE/abuse case, attack surface, threat→asset coverage | SEC-02 + SEC-01 | C4/DFD, STRIDE model, ADR, T-100 baseline | G02: непокрытая критическая граница → NO-GO |
| S03 — Algorithms and strict data contracts | 5, 11–12, 31 | functional process model | source-linked ALG IDs; component invariants; exact input/output schemas; recipient allowlist; fail-closed transformations; nested closed JSON | SEC-01, SEC-02 | `algorithm_contract.yaml`, `component_contract.yaml`, `flow_contract.yaml`, OpenAPI and policy impact | G03: неизвестное поле/получатель/алгоритм → REJECT |
| S04 — API and identity | 11, 14, 26, 31 | closed contracts | JWT/mTLS where justified, principal→agent→tool delegation; BOLA/BFLA; object ACL; TOCTOU approval hash; rate limits; idempotency | SEC-04 + SEC-02 | policy decisions, request/response schema tests, deny cases, API lifecycle | G04: BOLA, privilege escalation, unauthorized tool → BLOCK |
| S05 — Code & engineering | 5, 7, 10, 18 | approved contracts | secure coding, static checks (Semgrep/Bandit etc.), unit/property/fuzz tests, no eval/shell from model, dependency pinning, reviewed human commits | SEC-03 | tests, static scan, commits, per-component security record | G05: high-critical finding unmitigated → BLOCK |
| S06 — Supply chain and release build | 18–20 | reviewed code/model/data | SBOM, model/data licences, hash/provenance, CI isolation, signed image, offline registry, immutable promotion, secret scanning | SEC-03 | signed artifact manifest, scan reports, SLSA-style provenance | G06: unknown licence/unsigned artifact/unpinned source → NO-GO |
| S07 — Ingestion, KB and GraphRAG | 6, 12–13, 23 | source policy, allowlisted channels | sanitise untrusted content, quarantine, source evidence, tenant vector/graph ACL, edge provenance, atomic reindex & rollback | SEC-02, SEC-05 | dataset snapshot/hash, RAG corpus test, poisoned-doc suite, retrieval metrics | G07: poisoned source promoted/secret retrieved → BLOCK |
| S08 — Models, agent workflows and training | 7, 13, 17, 19, 27 | verified model + KB | scoped mission prompt, finite-step LangGraph, checkpoints outside Pod, curriculum, independent feedback/holdout, versioned updates | SEC-05 + SEC-04 | model card, training/eval splits, deterministic state transition traces | G08: agent self-approval, reward hack or unsafe act → BLOCK |
| S09 — Authorization and impact gate | 7, 14, 30–31 | output proposal with provenance | policy outside LLM, deny by default; verify semantic impact, human action approval, TOCTOU and tool allowlist, only bounded low-risk actions | SEC-04 | explicit ALLOW/DENY decision with parameters, audit, replay negative tests | G09: unauthorized consequence/tool call → STOP |
| S10 — Independent POLYGON qualification | 9, 13–14, 19, 30 | immutable candidate release | 100 threats linked to negative tests, mutation/metamorphic tests, sealed holdouts, security regression, requalification on changes | SEC-05 | executable test pack, hashes, independent report, qualification decision | G10: P0 failure or unsupported claim → NOT_QUALIFIED |
| S11 — Kubernetes/on-prem deployment | 15–18, 20–26, 28 | qualified build | isolated Docker/K8s, service accounts, CNI policy enforcement, Secrets encryption, image admission, Pod Security, GPU/DB/backup/DR, egress deny | SEC-03, SEC-06 | dry-run and live policy checks, network capture, restore and fault tests | G11: isolation fail/airgap breach → BLOCK |
| S12 — Operations, changes and decommission | 10, 15, 20–21, 24, 28–30 | approved runtime | telemetry, SOC, drift, anomaly, vulnerability re-scan, revocation, incident response, backups/retention, model upgrades, decommission | SEC-06 + SEC-01 + SEC-05 | SLO, incident tabletop, revoke tests, continuous regression evidence | G12: incident/unsafe drift → CONTAIN/REVOKE |

## Связь каждой фазы с каталогом TOP-100
| Группа каталога | THR IDs | Основной gate | Вторичные gates |
|---|---|---|---|
| GOV — управление и требования | THR-001…010 | G00–G02 | G10 |
| ALG — алгоритмы/контракты/API | THR-011…020 | G03–G04 | G09–G10 |
| IDM — роли, идентичности, полномочия | THR-021…030 | G04 | G09–G12 |
| KNW — источники, знания, GraphRAG | THR-031…040 | G07 | G08–G10 |
| AGT — агенты, действия, состояния | THR-041…050 | G08–G09 | G10 |
| ML — LLM, обучение и экзамен | THR-051…060 | G08 | G10–G12 |
| SUP — репозитории, поставка и сборка | THR-061…070 | G05–G06 | G11 |
| DAT — данные, события, приватность | THR-071…080 | G03/G07 | G09–G12 |
| K8S — инфраструктура и облако | THR-081…090 | G11 | G12 |
| OPS — эксплуатация и завершение | THR-091…100 | G12 | G10–G11 |

## Gate Decision — нормативная логика
- `NOT_STARTED`: документы/реализация отсутствуют.
- `DESIGNED`: требования и схемы утверждены на проектном уровне, но код/тест не исполнены.
- `TESTED`: зафиксирован исполнявшийся тест в описанной среде, review ещё возможен.
- `QUALIFIED`: независимые тесты и security review связаны с точной версией, результат подписан.
- `APPROVED`: человек-ответственный выпускает именно квалифицированный артефакт.
- `REVOKED`: текущий допуск недействителен. `STOP` для action, `ROLLBACK` только на заведомо квалифицированную безопасную версию.
Уровень доверия agent: T0…T4; autonomous high-risk outcomes **не входят в MVP**.

## Contract-Strict × угрозы
1. `FLOW-*` — фиксированные sender/receiver/purpose/schema version/classification/permission, данные по минимуму.
2. `ALG-*` — source, inputs/outputs, pre/post conditions, invariants, safe fallback; zero silent unknown fields.
3. `CMP-*` — version, owner, dependencies, fail mode, resource budget, audit and test evidence.
4. `ACT-*` — parameter hash, object version/TTL, policy ref, human consent ref, idempotency key and executor service identity.
5. `QUAL-*` — immutable test version, environment, result, examiner independence, artifact digest.
6. `INC-*` — trigger, containment, revocation, owner and recovery evidence.

## CI/CD minimum pipeline
`Requirements check → Contract validation → Algorithm tests → SAST/SCA/secrets → SBOM/licence → unit/property tests → offline build → image provenance/signature → API integration tests → adversarial RAG/LLM tests → Kubernetes admission & network tests → POLYGON independent qualification → human release approval`.

### Policy for critical findings
Любой провал P0 теста в применимой области: BLOCK promotion. Временное отступление по низшим рискам возможно только с письменным approval владельца риска, сроком, компенсирующими мерами и планом исправления. Отступления от запретов опасных действий, cross-tenant access и self-approval **не допускаются**.

## MVP execution priorities (not calendar promises)
- **Wave A:** G00–G04, строгие контракты, identity, trust boundary; закрыть 100% P0 в этих модулях.
- **Wave B:** G05–G07, offline build, SBOM, provenance, quarantined GraphRAG, secured object/events.
- **Wave C:** G08–G10, policy, human approvals, QUAL-01, independent negative tests and requalification.
- **Wave D:** G11–G12, offline Compose/K8s placement option, backup, incident response and measured cost.
For each wave, real cost and scope after actual P1 reuse audit and customer discovery. Each wave contributes exact output to OTUS final pack.

## 6 security roles / separation of duties
SEC-01 Security Architect: business risk owner liaison, requirements, acceptance.  
SEC-02 Threat Modeler: STRIDE, DFD, data/algorithm threat impact.  
SEC-03 DevSecOps: CI/CD, build provenance, IaC/K8s admission.  
SEC-04 Runtime Security: deterministic policy + authorized tool gateway.  
SEC-05 Independent Qualification: POLYGON and hidden holdout, separated from developing agent.  
SEC-06 Operations Security: SOC, revocation, monitoring and incident response.

Three MVP role-priorities: SEC-01, SEC-04, SEC-05. **Functions SEC-02/03/06 still must be covered** (humans/tools); not optional exclusions.

## Evidence Record (template)
```yaml
threat_id: THR-016
asset_id: object-registry
flow_id: FLOW-OBJECT-READ
algorithm_id: ALG-READ-001
component_id: CMP-OBJECT-API
test_id: NEG-THR-016
git_commit: TBD
artifact_sha256: TBD
environment: TBD
owner: SEC-04
reviewer: SEC-05
result: NOT_RUN
risk: UNASSESSED
release_gate: BLOCK_UNTIL_TESTED
```

## Источники
[NIST SP 800-218](https://csrc.nist.gov/pubs/sp/800/218/final); [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework); [OWASP Agentic 2026](https://genai.owasp.org/top-10-for-agentic-applications-2026/); [OWASP API 2023](https://api-security.owasp.org/editions/2023/en/0x00-header/); [MITRE ATLAS](https://atlas.mitre.org/); [SLSA](https://slsa.dev/spec/v1.2/); [Kubernetes Security](https://kubernetes.io/docs/concepts/security/security-checklist/).

**Фактическая готовность:** пока только спецификация. Нельзя считать список негативных тестов исполненным или утверждать, что закрыты 81 P0 угрозы.
