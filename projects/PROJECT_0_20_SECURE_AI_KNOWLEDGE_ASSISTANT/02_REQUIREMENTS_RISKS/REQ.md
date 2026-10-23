# Functional Requirements

| ID | Requirement | Acceptance |
|---|---|---|
| FR-001 | Система принимает текстовый вопрос | API accepts valid request and trace_id is created |
| FR-002 | Система получает identity/access context | unauthorized request is rejected |
| FR-003 | Retrieval фильтрует документы по access policy | forbidden fixture is never returned |
| FR-004 | Система извлекает top-k evidence | retrieval evidence stored in trace |
| FR-005 | Ответ формируется на основе context | response carries evidence references |
| FR-006 | Ответ содержит citations | every factual answer has source references or explicit “insufficient evidence” |
| FR-007 | При недостатке доказательств система не выдумывает ответ | abstention path is testable |
| FR-008 | PII/secret policy применяется до внешнего model call when required | policy test suite passes |
| FR-009 | Логи не содержат запрещённых raw secrets | automated log scan passes |
| FR-010 | Каждый ответ имеет audit correlation | trace_id links request, retrieval, model, output |
| FR-011 | Knowledge update создаёт versioned index | index version is recorded |
| FR-012 | Release binds app/model/index/prompt | release manifest validation passes |
| FR-013 | Production rollout supports Canary | 1% → 5% → 100% state machine |
| FR-014 | Failed candidate can return traffic to stable | rollback drill succeeds |

## Priority

FR-001..FR-010, FR-012..FR-014 = **Must**.  
FR-011 = **Must** for production, can be manual in early PoC with explicit evidence.
