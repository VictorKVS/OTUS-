# RISK-TRUST-001 — Risk Register, 6 Security Roles и независимая квалификация
## Роли
SEC-01 Security Architect — IDEA+ и risk/security requirements; SEC-02 Threat Modeler — HLD/LLD; SEC-03 DevSecOps — build/supply chain; SEC-04 Runtime Security Controller — каждое действие; SEC-05 Independent Examiner — квалификация и запрет self-approval; SEC-06 Security Monitoring Analyst — эксплуатация и инциденты.
Это функциональные роли, **не шесть готовых агентов**. Runtime allow/deny выполняет deterministic policy engine; квалификация изолирована от проверяемого агента.

## Risk Register
| ID | Риск | Серьёзность | Контроль | Gate |
|---|---|---|---|---|
| R-01 | ИИ классифицирует гражданский объект как опасный | CRITICAL | ABSTAIN, provenance, human review; no autonomous harmful acts | STOP |
| R-02 | Межарендаторная утечка через graph/vector/cache/log | CRITICAL | policy prefilter, graph traversal ACL, red-team User B | BLOCK release |
| R-03 | Prompt injection вызывает tool misuse | HIGH | tool gateway deny-by-default, schema validation | FAIL on bypass |
| R-04 | Изменения модели/промпта после экзамена | HIGH | version hashes, regression and trust revocation | REQUALIFY |
| R-05 | Слабое качество knowledge attribution | HIGH | source provenance, evidence scorer + heldout | RESEARCH |
| R-06 | Поздние/дублирующиеся события | MEDIUM/HIGH | event IDs, replay, idempotent action | REWORK |
| R-07 | GPU OOM или задержка при росте нагрузки | HIGH | measured capacity, limits, queue, circuit breaker | SLO gate |
| R-08 | Отсутствие юридических прав на модели/документы | HIGH | license and dataset inventory | NO GO |
| R-09 | Облако нарушает airgap или data policy | CRITICAL | OTUS local only; legal and architecture decision for other product | NO GO |
| R-10 | Непроверенное самообучение | HIGH | bounded feedback, review, rollback, independent eval | BLOCK |
| R-11 | Пользователь ожидает 20 готовых агентов от 20 YAML | HIGH | 3 separately qualified domains before scale | HONEST CLAIMS |
| R-12 | Экономика не учитывает человеческую проверку | HIGH | all attempt/review costs in TCO | REESTIMATE |

## Qualification states
T0 sandbox, T1 observe, T2 advise, T3 draft, T4 bounded reversible action after domain-specific test, T5 high-risk prohibited autonomy in MVP. Для каждого T state фиксировать модель, версию, онтологию, источники, инструменты, область, срок действия, выдающего и отзывающего.

## Monitoring and SLO
Metrics: failed ACL, policy denials, ungrounded claims, drift, false positives/negatives, retry loops, event duplication, audit failures, agent cost, p95/TTFT. Stale or absent evidence must trigger review, not silent approval.

## BPMN / UML / DMN
- [Lifecycle with 6 roles and RACI](../IDEA_PLUS_V0_2/13_SECURITY_ROLES_BUSINESS_ANALYSIS.md)
- [BPMN 2.0 process source](../IDEA_PLUS_V0_2/diagrams/security_lifecycle.bpmn)
- [UML Use Case](../IDEA_PLUS_V0_2/diagrams/security_use_cases.puml)
- [DMN decision table](../IDEA_PLUS_V0_2/diagrams/security_decision_table.md)

## Independent acceptance
Test user B secret; injection via retrieved material; human reject; expired qualification; tampered evidence; ambiguous civilian object; offline egress; restore/failover; adverse feedback. PASS does not imply universal safety; findings require requalification and stop triggers.
