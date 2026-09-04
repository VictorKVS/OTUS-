# Эволюция курса: ДЗ 01 → ДЗ 05 → ДЗ 07

## Почему это важно

Домашние задания рассматриваются не как независимые документы, а как последовательное развитие архитектурной компетенции.

При этом **ДЗ 01 и ДЗ 07 используют разные бизнес-кейсы**. Из первого задания наследуется не предметная модель, а **архитектурный метод**: сначала снимаем неопределённость и фиксируем бизнес-ценность, контрактную модель, риски и этапы проекта; затем уже проектируем C4/API и только после этого — AI/RAG/agents.

---

## ДЗ 01 — стратегия, риски и roadmap AI-проекта

Легенда первого ДЗ: крупный ритейлер хочет систему персонализированных рекомендаций, но исходное требование размыто: «хотим как у Ozon».

Задание требовало:

1. сформулировать 5–7 уточняющих вопросов клиенту;
2. выбрать и обосновать контрактную модель для PoC и основной разработки;
3. составить AI-specific risk matrix и mitigation plan;
4. разработать Roadmap с этапами PoC → MVP → Production и DoD для каждого этапа.

Статус: **принято**.

Сильная методическая сторона, которую сохраняем дальше: **числовые оценки должны быть объяснимыми** — иметь источник, расчёт, допущение или быть явно помечены как учебный threshold.

---

## ДЗ 05 — от требований к архитектурным контрактам

На следующем уровне неопределённость уже переведена в архитектурные артефакты:

- C2 Container Diagram;
- C3 Component Diagram;
- Sequence Diagram;
- OpenAPI 3.1;
- стабильный внутренний endpoint `POST /get_recommendation`;
- `evidence_refs`, `confidence`, `limitations`, `research_gaps`.

Таким образом, ДЗ 05 отвечает на вопрос: **как требования превращаются в границы системы и контракты взаимодействия?**

---

## ДЗ 07 — от контрактов к интеллектуальному ядру

ДЗ 07 использует уже освоенный процесс и добавляет:

- конкретный business-process командировки;
- `TripMission`, Institution, Venue и Approval;
- Supervisor / Multi-Agent architecture;
- Policy RAG и Vector DB;
- Hybrid Retrieval, reranking, chunk expansion;
- typed LangChain messages и `Command(goto=...)`;
- provider adapters;
- Human Approval перед Booking/Payment;
- CI quality gates.

Внутренний AI-контракт из ДЗ 05 **не заменяется**, а расширяется:

```text
POST /get_recommendation
recommendation_type = TRAVEL_PLAN
+ travel_context
+ domain_result = TripPlanResult
```

---

## Каноническая цепочка проектирования

```text
ДЗ 01
Бизнес-неопределённость
→ вопросы
→ контракт
→ риски
→ PoC / MVP / Prod

        ↓

ДЗ 05
C4
→ Sequence
→ API contracts
→ evidence-backed response

        ↓

ДЗ 07
Business Process
→ Multi-Agent Supervisor
→ Hybrid RAG
→ provider adapters
→ Human Approval
→ observability / eval
```

---

## Правило происхождения цифр

Для всех дальнейших заданий применяется единый стандарт:

```text
любая существенная цифра
→ источник / измерение / расчёт / допущение
→ статус достоверности
```

Примеры:

- срок PoC — из оценки объёма работ и команды;
- бюджет — из provider data + deterministic calculation;
- latency — из telemetry, а не «на глаз»;
- HitRate/MRR — из versioned eval dataset;
- risk score — из принятой шкалы Probability × Impact;
- SLA/SLO — из согласованных бизнес-требований.

Если источник отсутствует, цифра помечается как **ASSUMPTION** или **EDUCATIONAL THRESHOLD**, а не выдаётся за измеренный факт.

---

## Артефакты

- ДЗ 01: раздел курса `1. Пресейл, контракты и работа с требованиями...`.
- ДЗ 05: C4 / Sequence / OpenAPI `/get_recommendation`.
- ДЗ 07: [`API_EVOLUTION_DZ05_DZ07.md`](./API_EVOLUTION_DZ05_DZ07.md), [`RAG_FLOW.md`](./RAG_FLOW.md), [`AGENT_HANDOFFS.md`](./AGENT_HANDOFFS.md).
