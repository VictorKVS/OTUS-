# SADEQ — API Contract Pack v0.1
**Статус:** PROPOSED / NOT_IMPLEMENTED / NOT_SECURITY_QUALIFIED.  
**Процесс:** Contract-first design → review → mock → contract tests → implementation.

## Назначение
Публичный для корпоративных клиентов интерфейс SADEQ UAA и Agent Factory. Спецификация OpenAPI 3.1 определяет HTTP-контракты, но не заявляет наличие работающего сервера. Никакие endpoint не должны предоставлять произвольный доступ к shell, файловой системе или внутренним БД. Offline/on-prem — обязательная поставка OTUS.

## Документы
- [OpenAPI 3.1](openapi.yaml) — API и схемы сообщений.
- [Архитектурные правила, безопасность и примеры](API_ARCHITECTURE_AND_SECURITY.md).
- [Проверки контрактов и этапы реализации](API_TEST_PLAN.md).
- [Sequence запроса и утверждения действия](sequence.mmd).

## Области API
Channels / Observations, Objects / Events, Knowledge / Evidence, Agent Profiles / Runs, Action Proposals / Approvals, Qualification / Revocation.

**Главный контракт:** LLM может предложить действие, но не авторизовать собственный вызов инструмента. Политика проверяется на сервере и повторно непосредственно перед выполнением. Высокорисковые действия не поддерживаются.

## Связь с OTUS
Урок 05 LLD, 07 агенты, 11 интеграции, 12 данные, 14 Security by Design, 15 Observability, 23 EDA, 26 Multi-tenancy, 31 API как продукт. См. [PRD](../02_PRD_REQUIREMENTS_ACCEPTANCE.md), [Security BA](../../IDEA_PLUS_V0_2/13_SECURITY_ROLES_BUSINESS_ANALYSIS.md).
