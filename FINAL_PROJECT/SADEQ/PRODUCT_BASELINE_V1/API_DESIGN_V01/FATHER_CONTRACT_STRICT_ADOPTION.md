# API-STD-002 — FATHER Contract-Strict / Algorithm-Bound Data Flow для SADEQ

**Дата:** 27.11.2026 · **Статус:** DESIGN ADOPTION / NOT IMPLEMENTED.
**Нормативный первоисточник:** [FATHER-STD-API-001](https://github.com/VictorKVS/FATHER_CODEX/blob/main/docs/protocols/CONTRACT_STRICT_API_ALGORITHM_BOUND_DATA_FLOW_V1.md).

## Нельзя путать два разных основания
- **The Twelve-Factor App:** эксплуатационные принципы проектирования приложений и облачных сервисов.
- **FATHER Contract-Strict:** запрет приёма/обработки/передачи не предусмотренных утверждённым алгоритмом и информационным контрактом данных.
Первое не заменяет второе. Точное первоначальное содержание упоминавшегося списка **«12 правил FATHER» не установлено**, поэтому двенадцать правил не реконструируются.

## Обязательный pipeline проектирования
IDEA+ → функциональная схема → Component Contract → Data Flow Contract → Algorithm Contract → API/OpenAPI → policy/UAG → security review → tests/POLYGON → реализация → independent integration qualification → human-approved release.

## Предварительный анализ существующего `openapi.yaml`
1. `ObservationInput`, `AgentProfileInput`, `ActionProposalInput`: на верхнем уровне уже используется `additionalProperties: false` — это положительное начало.
2. `ObservationInput.payload`: сейчас `type: object` без поля `additionalProperties: false`, следовательно, допускает произвольные вложенные данные. **Контракт-строгий критерий НЕ ВЫПОЛНЕН**, пока нет реестра схем `source_id + kind + version`, ограничений глубины и body size.
3. `ObjectState.state` и `KnowledgeResult`: текущие схемы не ограничивают все допустимые поля; для границ доверия необходим отдельный domain-specific output schema.
4. `ActionProposalInput.action_type`: открытая строка; нужно связывание с версионированным registry allowlisted operations и schema конкретной операции.
5. `/agents/{agentId}/runs` принимает свободную цель — допустимо как недоверенный текст для reasoning, **не** как полномочие расширить tools.
6. `approved` — не равно `executed`. Нужны утверждённый scope, TTL, однократность, отдельный service identity и повторный check перед действием.
7. В текущем проекте **не выполнены контрактные tests и независимый POLYGON**. Нельзя считать требования FATHER реализованными только потому, что схема записана в репо.

## Модель FLOW-001
```yaml
flow_id: FLOW-001
sender: channel-adapter
receiver: observation-service
purpose: register-validated-observation
algorithm_id: ALG-OBS-NORMALIZE-001
schema_id: observation.stock_change.v1
allowed_fields:
  - source_id
  - external_key
  - observed_at
  - kind
  - payload.stock
permissions: [observations:write]
side_effects: [append-observation]
data_owner_policy: object-tenant-label
on_unknown_field: REJECT
on_unknown_operation: DENY
on_unauthorized_recipient: DENY
evidence_required: [positive-contract-test, negative-field-test, acl-test]
```

## Security/Qualification acceptance
- unknown field on input/output; nested unknown field; cross-tenant document; unauthorized recipient; direct DB bypass; prompt asks to change schema; stale contract, model or agent-version; external egress; idempotent retry.
- On violation: STOP / DENY / ABSTAIN, no tool call, audit of rejection without secrets.
- Change control: CR → algorithm/schema impact → SEC review → new contract version → independent test → human sign-off.

## Change management
This addendum is an explicit requirement to **revise** the previously published OpenAPI v0.1, rather than retroactively claiming it is already contract-strict. New API v0.2 should use full component schema registry, Pydantic strict mode, JSON Schema `additionalProperties: false` at all applicable nested levels, authorization before retrieval/tool, and separately constrained data-plane APIs.
