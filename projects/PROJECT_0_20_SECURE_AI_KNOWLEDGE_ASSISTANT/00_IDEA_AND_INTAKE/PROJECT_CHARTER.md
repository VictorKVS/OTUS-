# Project Charter · Secure AI Knowledge Assistant

**Project ID:** SAIKA-001  
**Stage:** 00 · Idea / Intake  
**Maturity:** M1 DESIGN  
**Owner:** FATHER Architect OS training project

## 1. Проблема

Сотрудник тратит время на поиск ответа по разрозненным корпоративным документам. Обычный поиск возвращает документы, но не гарантирует, что пользователь быстро найдёт нужный пункт и поймёт, на какой источник опирается ответ.

## 2. Идея

Создать защищённого AI‑ассистента, который:

1. принимает вопрос сотрудника;
2. определяет доступный пользователю контур знаний;
3. извлекает релевантные фрагменты;
4. формирует ответ только на основе разрешённого контекста;
5. показывает ссылки/цитаты на источники;
6. применяет PII/security/guardrail policies;
7. сохраняет технический audit trail;
8. поддерживает versioned release и rollback.

## 3. Необходимый результат

Не «чат с LLM», а управляемый сервис:

```text
QUESTION
→ ACCESS POLICY
→ RETRIEVAL
→ RERANK
→ CONTEXT
→ LLM
→ OUTPUT VALIDATION
→ CITATIONS
→ AUDIT
```

## 4. Scope v1

**Входит:** текстовые документы, RAG, цитирование, API, базовый UI, auth context, observability, evaluation, security controls, CI/CD, MLOps/knowledge refresh, Canary release.

**Не входит в v1:** автономное выполнение финансовых/юридически значимых действий; обучение foundation model с нуля; unrestricted web browsing; голос/видео; массовая генерация документов.

## 5. Главные архитектурные свойства

| Свойство | Почему важно |
|---|---|
| Grounded answers | ответ должен быть связан с источником |
| Access-aware retrieval | нельзя выдавать данные из чужого контура |
| Reproducibility | любой релиз воспроизводим по версиям |
| Observability | можно понять, почему релиз деградировал |
| Replaceability | model/RAG/eval/security blocks сменные |
| Rollbackability | предыдущий stable остаётся доступным |

## 6. Definition of Done для проекта 0–20

Проект считается завершённым на уровне курса, когда traceability связывает:

```text
BUS → REQ/NFR → RISK → ADR → ARCH → DATA/RAG
→ SECURITY → EVAL → SLO → SIZING
→ CI/CD → MLOPS → RELEASE → ROLLBACK
```

и каждый числовой gate имеет provenance: COURSE / SOURCE / LAB / PROD.
