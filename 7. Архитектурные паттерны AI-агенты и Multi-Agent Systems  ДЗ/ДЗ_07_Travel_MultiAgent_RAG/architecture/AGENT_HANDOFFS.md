# Agent Messages & Handoffs — M1.1

## Зачем это добавлено

Критерий ДЗ требует, чтобы агенты не просто существовали на диаграмме, а реально обменивались сообщениями. Поэтому M1.1 использует штатную модель сообщений LangChain/LangGraph вместо самодельного списка словарей.

## Состояние

```python
class TravelState(MessagesState):
    request: dict
    policy_hits: list
    expanded_policy_chunks: list
    retrieval_metrics: dict
    flight_options: list
    hotel_options: list
    budget: dict
    final_answer: dict
```

`MessagesState` хранит типизированную историю сообщений и применяет reducer для поля `messages`.

## Типы сообщений

- `SystemMessage` — системные правила demo: read-only, no real booking, evidence required.
- `HumanMessage` — исходный запрос сотрудника.
- `AIMessage(name="manager")` — решение координатора и handoff.
- `AIMessage(name="policy_rag")` — результат RAG поиска и evidence refs.
- `AIMessage(name="flight_search")` — варианты перелёта.
- `AIMessage(name="hotel_search")` — варианты проживания.
- `AIMessage(name="budget_analyst")` — бюджет и policy check.

## Явные handoff через `Command`

```text
Manager
  │ Command(goto="policy_rag")
  ▼
Policy RAG
  │ Command(goto="flight_search")
  ▼
Flight Search
  │ Command(goto="hotel_search")
  ▼
Hotel Search
  │ Command(goto="budget")
  ▼
Budget Analyst
  │ Command(goto="finalize")
  ▼
Manager / Finalize
```

Каждый `Command` одновременно:

1. добавляет типизированное сообщение в state;
2. обновляет доменные данные результата агента;
3. фиксирует trace события;
4. явно задаёт следующий узел.

## Почему Supervisor

Manager хранит общий контекст и оркестрирует специализированные агенты. Это сохраняет Single Responsibility: Policy RAG не ищет билеты, Flight Search не трактует корпоративную политику, Budget Analyst не меняет результаты поиска.

## Проверка

`tests/test_demo.py` проверяет:

- наличие `SystemMessage`, `HumanMessage`, `AIMessage`;
- имена всех специализированных агентов в message history;
- последовательность `Command` handoff в trace;
- возврат финального результата обратно Manager.

## Первоисточник

LangChain messages reference:
https://reference.langchain.com/python/langchain/messages
