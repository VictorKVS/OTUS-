# SADEQ Secure SDLC + TOP-100 Threat Catalog v1.0
**Дата:** 27.11.2026 · **Статус:** DOCUMENTED, NOT_IMPLEMENTED, TESTS_NOT_RUN.

## Результаты
- [13 фаз безопасной разработки G00–G12, роли, тесты и GO/NO-GO](SECURE_SDLC_ROADMAP.md).
- [100 проектных сценариев угроз с защитами и отрицательными тестами](TOP_100_THREATS.md).
- [CSV реестр 100 угроз для импорта в SecGraph/Excel/Jira](TOP_100_THREATS.csv).

## Область
IDEA+, бизнес-процессы, алгоритмические контракты, API, UAG, агентные действия, ALINA / RAG / knowledge graph, independent POLYGON, secure coding, supply chain, Kubernetes, GPU, данные/PII, continuous trust, incident response.

## Количество
100 уникальных проектных строк: 10 классов по 10. Первоначальный приоритет: **81 P0**, **19 P1**; это инженерный план и ещё не утверждённая количественная оценка вероятности и влияния. Понижение или повышение приоритета требует решения владельца риска и evidence.

## Главное правило
`REQ → RISK/THR → ALG+FLOW+COMPONENT_CONTRACT → CTRL → NEGATIVE_TEST → EVIDENCE → INDEPENDENT_QUALIFICATION → HUMAN_APPROVAL → RELEASE`.

Вся релевантная угроза P0 требует контроля и реально пройденного теста перед активацией затрагиваемой функции. `READMEs, test plans, source files` не равны доказательству готовности.

## Проектные связи
- [FATHER Contract-Strict](https://github.com/VictorKVS/FATHER_CODEX/blob/main/docs/protocols/CONTRACT_STRICT_API_ALGORITHM_BOUND_DATA_FLOW_V1.md).
- [SADEQ Product Baseline](../00_PRODUCT_DOCUMENT_REGISTER.md).
- [Six security roles / BPMN / UML / DMN](../../IDEA_PLUS_V0_2/13_SECURITY_ROLES_BUSINESS_ANALYSIS.md).
- [OpenAPI Contract Pack](../API_DESIGN_V01/README.md).
- [Twelve-Factor/Kubernetes as additional infrastructure methodology](../K8S_12_FACTOR_V01/README.md).

## Следующий проверяемый шаг
Разобрать **THR-011..020 (ALG/API)** и **THR-021..030 (identity/ACL)** на фиксированных примерах OpenAPI/JSONSchema/UAG. Выполнить 20 негативных тестов в изолированном mock/staging, сохранить evidence (сборка, хэш версии, лог и подтверждение независимого экзаменатора). Сейчас эти тесты **не исполнены**.

## Правовая и этическая граница
В реестре представлены только защитные меры и сценарии тестирования. Автономная классификация целей и применение силы исключены; сомнительная классификация гражданского объекта требует ABSTAIN и независимой проверки.
