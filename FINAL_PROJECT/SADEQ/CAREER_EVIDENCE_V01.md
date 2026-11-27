# SADEQ — Корпоративная инженерная квалификация и карьерное портфолио
**Версия:** 0.1 · **Дата:** 2026-11-28 · **Статус:** PLAN / EVIDENCE INCOMPLETE.

## Цель
Показать работодателю не красивые диаграммы, а подтверждённую способность инженера/архитектора провести enterprise AI-интеграцию от бизнес-потребности до контролируемого релиза. Реальные полномочия и роль автора в проекте описывать точно; учебную лабораторию не выдавать за внедрение у заказчика.

## Проблемы корпорации и инженерное решение SADEQ
| Проблема / вопрос работодателя | Инженерное решение | Чем это доказать | Текущее состояние |
|---|---|---|---|
| Пользователи тратят время на поиск решения ITSM | ConOps + регулируемый RAG + citations | paired benchmark vs manual/nonagent search, valid source refs | DESIGNED; no measured impact |
| Неуправляемый AI может вызвать опасное действие | отдельный детерминированный UAG + human approval | negative tool bypass and stale approval tests | DESIGNED; mock prototype partial |
| Подмена tenant/IDOR в API | AuthContext, per-object/property ACL, strict schemas | API-001 protocol + multi-tenant isolation evidence | PMI DESIGN; NOT_RUN |
| API сторонней ITSM отказывает/возвращает 200 без эффекта | outbox, idempotency, EXECUTION_UNKNOWN, authoritative read-back | fault injection, replay, verified state evidence | DESIGNED |
| Требования теряются между разработкой и QA | requirements traceability FR→FLOW→ALG→THR→TEST→EVI | approved traceability register, signed results | MATRIX DRAFT |
| LLM отвечает без подтверждений | approved corpus, source version, retrieval evidence | Recall@k, citation support rate, injection eval | PLANNED |
| Зависимость от зарубежного облачного LLM | on-prem inference & restricted egress | documented model licensing, packet/log test, GPU benchmark | PLANNED |
| Нельзя доверять тестам, которые написал сам агент | POLYGON independent holdout and release owner | independent candidate hash, test logs and reviewer | PLANNED |
| Непонятна эксплуатационная стоимость/риски | performance p95, TTFT, RAM/VRAM, RTO/RPO, TCO | reproducible workload and runbooks | PLANNED |
| Заказчик требует формальные испытания и документацию | ГОСТ-ориентированные ТЗ, эскизный/техпроект, ПМИ/протокол | approved set, exact test evidence and signoff | DRAFT |

## Артефакты, которые должно быть возможно продемонстрировать за 10–15 минут
1. Business scenario: INC-001 and reason for agent; show no artificial ROI.
2. Architecture: trust boundaries C4, B01–B08, why UAG independent from LLM, ADR tradeoffs.
3. Contract: request+response+negative MUST NOT, source/book/standard mapping, version.
4. API threat: reproducible BOLA/tenant spoof attempt: reject + no data or side effects.
5. Positive action: citing SOP → typed proposal → human approval → mock ITSM → verify state.
6. Negative action: injection/stale approval/HTTP200-mismatch → fail closed.
7. Independent evaluation: POLYGON run and exact candidate hashes, redacted reports.
8. Business measurement: actual p95/time/cost only if measured and same workloads.
9. Code quality: Python tests, GitHub commits, CI, SBOM, ADR, signatures.
10. Documentation discipline: project/TZ/PMI revision and requirement-to-evidence link.

## Employer questions to rehearse
- Why can't JSON Schema replace object-level authorization?
- What is difference between authentication, OAuth delegation and business-policy decision?
- What happens if an external ITSM side effect succeeded but response timed out?
- Why can't the agent approve its own action or qualification?
- When choose PostgreSQL transaction/outbox vs direct network call?
- How does retrieval enforce per-tenant permissions across cache and vector store?
- How to compare candidate local models under 12GB VRAM and quality constraints?
- How do you show evidence that a failed negative test blocked release?
- What normative sources and which exact clauses guided each test?
- What compromises can the customer accept, and which are mandatory release blockers?

## Interview truth protocol
- `DESIGNED` = architecture, source, contract, approved requirement not guaranteed.
- `IMPLEMENTED` = source and deployed component exists and can run.
- `TESTED` = reproducible test result with exact environment and evidence.
- `QUALIFIED` = independent process with frozen candidate, evidence and human review.
- `PILOT` = permissioned corporate environment and genuine user feedback.
Never claim employer deployment or validation based only on diagrams, unit tests or LLM-generated summaries.

## Next practical gate
Finish [formal PMI](TEST_ENGINEERING_V01/README.md) review → transform API-001/002/003 into executable security tests → implement verified identity/ACL and stable FastAPI contract → collect Windows lab evidence → expand to real data/RAG/UAG and POLYGON.
