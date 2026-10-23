# Метрики, пороги и доказательная база

## 1. Правило

Порог считается пригодным для production только после трёх уровней подтверждения:

| Уровень | Что означает | Можно использовать для blocking gate |
|---|---|---|
| SOURCE | подтверждённая инженерная практика/стандарт | как метод, но не обязательно как конкретное число |
| LAB | воспроизводимый controlled test | для учебного gate и initial calibration |
| PROD | измерен на реальном сервисе и связан с SLO/error budget | да |

## 2. Что задано самим ДЗ

| Параметр | Значение | Основание |
|---|---:|---|
| Canary stages | 1% → 5% → 100% | прямое требование Lesson 20 |
| CI/CD skeleton | Commit → Build → Unit → Staging → E2E → Prod | прямое требование Lesson 20 |
| Model Registry link | обязателен | критерий «Интеграция» |
| Rollback strategy | обязательна | критерий «Безопасность релиза» |

## 3. Что подтверждено инженерной практикой

Google SRE описывает canary как частичное и ограниченное по времени развёртывание с оценкой перед продолжением rollout. В их worked example 5% canary при 20% ошибочных запросов даёт около 1% общей error rate, что иллюстрирует линейное снижение blast radius при равномерном трафике.

Argo Rollouts позволяет строить analysis gates на Prometheus metrics; официальный пример использует success-rate condition и failure limit. Это подтверждает сам механизм metric-driven promotion/abort, но **не делает 95% универсальным production SLO**.

NIST AI RMF / TEVV требуют измеримости, test/evaluation и мониторинга AI в жизненном цикле; конкретные quality thresholds должны зависеть от контекста применения.

## 4. Статистический дизайн A/B

Canary и A/B разделены:

- **Canary** отвечает: «безопасно ли продолжать релиз?»
- **A/B** отвечает: «вариант B действительно лучше A по выбранной метрике?»

Для бинарной метрики при baseline 80%, ожидаемом улучшении до 85%, двустороннем α=0.05 и power=0.80 нормальное приближение даёт примерно **906 наблюдений на вариант**. Это пример power calculation, а не универсальное число.

Следствие: нельзя писать «подержим canary 10 минут» без RPS. Окно определяется тем, сколько наблюдений необходимо собрать и покрывает ли оно естественную вариативность нагрузки.

## 5. Лабораторная calibration

Controlled lab с фиксированным seed, 10 000 synthetic requests на stable и 10 000 на candidate:

| Metric | Stable | Candidate | Difference |
|---|---:|---:|---:|
| success rate | 99.58% | 99.49% | -0.09 п.п. |
| error rate | 0.42% | 0.51% | +0.09 п.п. |
| p95 latency | 319.01 ms | 330.78 ms | +3.69% |
| p99 latency | 402.64 ms | 416.47 ms | +3.44% |
| mean latency | 191.34 ms | 196.79 ms | +2.85% |

Это **LAB evidence**, не production evidence. Скрипт находится в `LAB/canary_calibration.py`.

## 6. Production gate design

Вместо произвольного «p95 не хуже 20%» используем следующую схему:

| Signal | Gate |
|---|---|
| Availability / errors | не нарушает SLO/error budget и statistically worse candidate не принимается |
| Latency | candidate сравнивается со stable на одном временном окне; порог задаётся NFR/SLO |
| AI quality | regression test на versioned golden set + confidence interval |
| Security | 0 critical confirmed security/data-leak events |
| Cost/request | укладывается в approved unit-economics budget |
| Saturation | CPU/RAM/GPU/queue не выходят за capacity policy |

Так цифры остаются воспроизводимыми и защищаемыми на проверке.
