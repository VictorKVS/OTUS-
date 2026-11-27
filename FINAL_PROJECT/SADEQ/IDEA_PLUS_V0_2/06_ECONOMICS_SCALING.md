# ECON-001 · Масштабирование и экономические последствия
**Затраты ниже — проектные параметры и учебные сценарии, не подтверждённые рыночные цены.**
## Три отдельных масштаба
1. **Разнообразие агентов:** агентные профили, онтологии, учебные наборы, инструменты, security tests. 20 конфигураций ≠ 20 качественно квалифицированных продуктов.
2. **Интенсивность обработки:** одновременно работающие LLM-запросы, GPU/KV-cache, batching, очереди, кэш. 20 агентов ≠ 20 физических GPU.
3. **Организации и контуры:** tenant isolation, локальная поставка, сопровождение, повышенная доступность, регламентный аудит.
## Поэтапная стоимость
| Шаг | CAPEX / разработка | OPEX / эксплуатация | Stop / Trigger |
|---|---|---|---|
| 0. IDEA+ | исследование, интервью, эксперименты | учёт и корректировка гипотез | нет business case |
| 1. Architecture | бизнес-модель, BPMN, C4, ADR, APIs | документация, contract reviews | нет трассировки требований |
| 2. Offline UAA | оборудование / разработка ядра | энергия, инференс, обслуживание | не проходит offline smoke |
| 3. GraphRAG | индексация и инфраструктура | embedding, reindex, backup | нет улучшения accepted outcomes |
| 4. Trust & security | RBAC, guardrails, audit, тесты | инциденты, QA, retention | ACL breach → BLOCK |
| 5. Learning/evaluation | goldens, reviewers, curriculum | мониторинг/drift/повторные экзамены | регрессия > порога |
| 6. Factory | генератор конфигураций / реестр | поддержка ABI и SDK | стоимость специализации > standalone |
| 7. 3 домена | онтологии, адаптеры, метрики | экспертиза и compliance | нет различий от prompt-wrapper |
| 8. 20 профилей | templates, миграции, обучение персонала | regressions, monitoring | регистрация без qualification |
| 9. HA / GPU pool | новая GPU/сервер/сеть/DR | питание, резерв, SRE | переход только при нарушении SLO |
| 10. Продукт | installer, лицензирование, support | поддержка и SLA | negative margin |

## Параметризованные формулы
`TCO_month=CAPEX_amortization+power+cooling+staff+security+qualification+backup+licenses+support`.
`Cost_per_qualified_outcome=total_cost_of_attempts / independently_accepted_outcomes`.
`Standalone_dev(N)=N×C_independent`.
`Factory_dev(N)=C_shared_core+N×C_specialization`.
`N_break_even=ceil(C_shared_core/(C_independent-C_specialization))` при положительном знаменателе.
Нулевая успешность → стоимость принятого результата неопределена, не 0.

## ТОЛЬКО ИЛЛЮСТРАЦИЯ
600 часов на ядро, 200 часов независимый агент, 40 часов новая специализация. 4 агента: 760 против 800 часов; 20 агентов: 1 400 против 4 000 часов (2 600 часов экономии при допущениях). При ставке 2 000 ₽/час: 2,8 млн ₽ против 8 млн ₽, разница 5,2 млн ₽, **исключая инфраструктуру, высокорисковые тесты, лицензии, интеграции и сопровождение**. Реальная точка окупаемости пока UNKNOWN.

## Стратегии
Quantization, small/large model routing, bounded agent loops, selective GraphRAG, cache with tenant-aware keys, GPU batching/queue, DB sharding, replication, failover. Каждый переход требует расчёта **quality-adjusted** incremental TCO и стресс-тестов на пиковых данных.

## Economic gates
LOW/BASE/HIGH нагрузка, фактические capex/opex, три модели качества, sensitivity ±50%, cost per accepted result, договорённые бюджетные пределы, estimate provenance, человеческое решение при выходе за лимиты.
