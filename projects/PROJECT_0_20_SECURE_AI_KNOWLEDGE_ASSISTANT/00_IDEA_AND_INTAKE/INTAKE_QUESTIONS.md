# Intake Questions & Assumptions

## 1. Что уже известно

| Область | Текущее решение |
|---|---|
| Пользователь | внутренний сотрудник организации |
| Основной сценарий | вопрос по внутренним документам |
| Ответ | краткий ответ + источники |
| Knowledge source | корпоративный документный контур |
| Delivery | API + web UI |
| Production target | Kubernetes/GitOps-compatible |
| Security | access-aware retrieval + PII/secret protection |

## 2. Что нельзя выдумывать

До интервью с заказчиком остаются открытыми:

- фактическое число пользователей;
- реальный RPS и concurrency;
- объём и прирост документов;
- типы документов и доля сканов;
- требования по on-prem/cloud;
- классы конфиденциальности;
- точный retention;
- допустимый monthly OpEx;
- юридически значимые ограничения;
- реальный baseline времени поиска;
- допустимые production SLO.

## 3. Course-source checklist

Из Presale AI Questionnaire Lesson 2 для проекта обязательно должны быть собраны ответы по пяти группам:

1. business context/value;
2. data/knowledge;
3. infrastructure/security;
4. integration/UX;
5. process/acceptance.

До получения фактов такие поля помечаются `TBD`, а не заполняются предположениями.
