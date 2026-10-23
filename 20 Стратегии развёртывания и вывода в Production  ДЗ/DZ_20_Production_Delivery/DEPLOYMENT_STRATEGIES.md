# Deployment Strategies · Rolling / Blue-Green / Canary

## Сравнение

| Strategy | Механизм | Плюсы | Ограничения | Где применяем |
|---|---|---|---|---|
| Rolling | экземпляры заменяются постепенно | просто, экономно по capacity | некоторое время coexist versions; быстрый полный rollback не всегда возможен | низкорисковые stateless changes |
| Blue-Green | одновременно существуют old/new environments; traffic switch | быстрый cutover и быстрый возврат | почти двойная capacity; state compatibility обязательна | крупные релизы, требующие мгновенного switch |
| Canary | candidate получает малую долю traffic с gates | минимизирует blast radius; позволяет сравнивать live metrics | нужен traffic router, observability и analysis logic | выбран для AI-service |

## Почему для AI Knowledge Assistant выбран Canary

AI-сервис имеет несколько независимых источников регрессии:

- application code;
- model version;
- RAG index / embeddings;
- prompt/config;
- external provider behavior;
- data freshness;
- safety/guardrail policy.

Canary позволяет ограничить влияние новой комбинации artifacts и остановить rollout до 100%.

## Blue-Green как fallback strategy

Blue-Green остаётся допустимой альтернативой, когда:
- нужен почти мгновенный cutover;
- достаточно capacity для двух окружений;
- state/data contracts совместимы;
- метрики можно проверить до переключения.

## Rolling

Rolling подходит для простых stateless releases, но хуже соответствует учебной задаче Lesson 20, поскольку OTUS прямо требует Canary plan с traffic stages 1% → 5% → 100%.
