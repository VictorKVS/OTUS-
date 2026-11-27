# SADEQ-ANALOG-001 — Аналитическая справка о мировых и российских аналогах
**К ТЗ SADEQ-TZ-003, редакция 0.3** · **Обзор на 28.11.2026** · **Статус:** MARKET BENCHMARK / RESEARCH, NOT PRODUCTION EVIDENCE.

## 1. Цель и корректная формула позиционирования
Сформировать документ-обоснование, почему выбран корпоративный IT Service Desk Copilot, какие проверяемые функциональные и эксплуатационные требования исходят из мировой практики, и что нужно доказать для конкурентоспособного **российского локального** продукта.

**Не допускается:** «лучше всех», «безопаснее ServiceNow», «отечественное импортозамещение достигнуто», «превзошли аналог» без одного workload, независимых испытаний и одинакового определения метрик. `DESIGNED` ≠ `IMPLEMENTED` ≠ `MEASURED`.
**Правильный тезис:** «SADEQ проектируется как локально развёртываемый AI Operations Copilot с проверяемой цепочкой решений, строго ограниченными действиями UAG и независимой квалификацией POLYGON; ожидаемые отличия должны быть подтверждены испытаниями».

## 2. Международные продукты и опубликованные кейсы (первичные источники)
| AN | Аналог / контекст | Публикуемый результат или функция | Что на самом деле измерено | SADEQ соответствие | Источник |
|---|---|---|---|---|---|
| AN-01 | ServiceNow Now Assist, собственная служба поддержки (Now-on-Now) | 89% запросов самообслуживания **поддерживаются** AI/automation; 37% операций в workflow обработки кейсов автоматизированы; 60% статей БЗ создаются AI | доля затронутых self-service запросов и операций; **не** полная доля автономно закрытых тикетов | Функциональный P0 аналог: классификация, KB, предложения и metrics | https://www.servicenow.com/uk/customers/now-on-now-support-ai.html |
| AN-02 | Moveworks + Broadcom, корпоративная IT-поддержка | 88% автономного разрешения support requests по сообщению поставщика (2025), исходно ~10%; более 75 000 IT issues resolved cumulatively | результат в конкретной среде Broadcom; не обобщён на другие отрасли и уровни критичности | Целевой ориентир для self-service; SADEQ сначала только assistive flow с human gate | https://www.moveworks.com/us/en/customers/broadcom-integrates-it-knowledge-base-with-moveworks-ai |
| AN-03 | mobilezone Supporto / Microsoft Copilot Studio, внутренний IT Service Desk | ~350 employee chats/mo; engagement 87%; ожидание разрешения инцидентов сокращено вдвое (по описанию Microsoft) | chats, engagement и время в кейсе mobilezone; 87% — **не** resolution rate | Наиболее близкая спецификация: ITSM Jira API, прикреплённые PDF/Word, Confluence KB, контекст заявки | https://github.com/MicrosoftDocs/power-platform/blob/main/power-platform/guidance/case-studies/mobilezone-modernizes-service-delivery.md |
| AN-04 | Salesforce Agentforce IT Service | более 180 организаций **выбрали** продукт за первые 4 месяца после GA (публикация 26.02.2026) | коммерческое принятие, **не** productivity или resolution rate | Конкурентная категория enterprise ITSM agents и CMDB; бизнес-эффект SADEQ сравнивать после пилота | https://www.salesforce.com/news/press-releases/2026/02/26/agentforce-it-service-selected-for-itsm/ |
| AN-05 | Atlassian Service Collection / Rovo | сообщается о ~70% сжатии alert noise и 6x ускорении формирования post-incident review в опубликованных кейсах | разнородные сценарии, не универсальный KPI Rovo | Будущая AI Operations специализация, incident evidence и postmortem | https://www.atlassian.com/blog/announcements/shareholder-letter-q3fy26 |
| AN-06 | Microsoft Copilot Studio, методика измерений | стандартизированная библиотека engagement, resolution, deflection, groundedness, citation accuracy, tool success | **методика метрик**, не результаты внедрения | Создать общую локальную KPI ontology; не смешивать unsupported/automated/resolved | https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/agent-business-value-metrics-reference |

## 3. Российский рынок: реальные альтернативы
| RU | Продукт | Подтверждено | Следствие для SADEQ | Источник |
|---|---|---|---|---|
| RU-01 | Naumen Service Desk + AI assistants | интеграция с заявками, локальной БЗ/историей; заявлена установка в **полностью изолированном** контуре, on-prem; заявлена сертификация ФСТЭК 4 УД для *Naumen Service Desk* (не автоматически для каждого AI-компонента) | **нельзя** называть on-prem уникальной функцией SADEQ; нужно сравнивать по качеству, прозрачности и доказательствам | https://www.naumen.ru/products/service_desk/ai_assistants/ |
| RU-02 | Yandex AI Studio On-premises | инфраструктура AI приложений может разворачиваться в контуре организации, включая GPU, API, моделирование/агентов | российская on-prem платформа уже существует; SADEQ должен выигрывать не как «ещё один model hub», а как узкий safety-qualified ITSM workflow | https://aistudio.yandex.ru/ru/docs/ai-studio/onprem/delivery-scope |
| RU-03 | GigaChat Enterprise / Just AI Agent Platform / MWS AI Agents | перечислены отраслевым исследованием как российские платформы создания AI-агентов, не все являются готовым Service Desk продуктом | различать платформенных конкурентов и прикладные ITSM-пакеты, не утверждать, что аналога в России нет | https://yakovpartners.com/publications/ai-agents-hype/ |
| RU-04 | Российские ITSM-внедрения Naumen | есть документированные проекты в РФ и СНГ; работающие процессы заявок/CMDB/инфраструктуры | требования совместимости с отечественным корпоративным стеком как отдельный пилотный контракт | https://www.naumen.ru/products/service_desk/ |

## 4. Сравнительная функциональная матрица
**Легенда:** `P` — публично описано у аналога; `D` — **только спроектировано** для SADEQ; `?` — публичных данных недостаточно; `E` — будет проверено после реализации. Это не security-аудит конкурентов.
| Критерий | ServiceNow | Moveworks | Microsoft Supporto | Naumen | SADEQ |
|---|---|---|---|---|---|
| Корпоративные IT-обращения | P | P | P | P | D(P0) |
| Поиск по KB и контекст заявки | P | P | P | P | D(P0) |
| API-действия и интеграции | P | P | P (Jira) | P | D(P0 mock ITSM) |
| Human handoff / управляемый workflow | P | P | P | P | D(P0) |
| Размещение в полностью локальном контуре | ? (зависит от поставки) | ? | ? | P | D(P0) |
| Strict algorithm-to-flow closed-schema | ? | ? | ? | ? | D(P0) |
| Независимый POLYGON с реальным evidence | ? | ? | ? | ? | D(P0) |
| Подтверждённый эффект в реальной корпорации | P | P | P | P (кейсы ITSM) | **нет** |
| Формальная сертификация/приёмка | зависит от конкретного продукта | ? | ? | заявлена сертификация Naumen SD | **нет** |

**Предостережение:** отсутствие открытого подтверждения `?` **не означает**, что конкурент лишён функции. Нельзя приписывать конкурентам отсутствие защиты лишь потому, что её нет на маркетинговой странице.

## 5. Где SADEQ должен превзойти baseline — гипотезы, не результаты
| DIFF | Проверяемая цель | Что надо создать | Как подтвердим |
|---|---|---|---|
| DIF-01 | Объяснимая история решения от сообщения до ITSM-результата | Object/Event Core, RAG citations, full trace | E2E trace includes exact source/version/decision/postcondition |
| DIF-02 | Отказ от незарегистрированных данных и действий | Closed JSON schemas, recipient/ALG allowlist, deterministic UAG | Negative injection/cross-tenant/tool-bypass suite; actual blocked calls |
| DIF-03 | Независимая квалификация конкретной версии | Immutable test suite, POLYGON, evidence signing | Independent re-run, version/hash matches, change invalidation |
| DIF-04 | Offline без зависимости от внешних AI API | Local inference + local data + restricted egress | Tested deny-all network profile, packet/eBPF capture where applicable |
| DIF-05 | Сниженные издержки интеграции с существующей ITSM | Stable adapters, mock-first, API contract tests | Time to integrate a *new* test adapter in equal conditions |
| DIF-06 | Российские корпоративные требования к документам и безопасности | ГОСТ-ориентированные документы, risk register, permission map | Independent documentation checklist and security review; no claim of military certificate |
| DIF-07 | Качество и скорость не хуже chosen baseline при равных данных | RAG/eval, agent workflow, local GPU measurements | Paired benchmark: same corpus, cases, rules, HW, acceptance metric |

## 6. KPI-онтология: не путать числители и знаменатели
| KPI-ID | Название | Определение SADEQ (проект) | Источник сравнения |
|---|---|---|---|
| KPI-01 | Verified outcome rate | число полностью подтверждённых выполненных заявок / число **разрешённых** тестовых заявок, подлежащих исполнению | SADEQ E2E |
| KPI-02 | Correct citation rate | ответы с подтверждёнными проверяющим ссылками на точный source chunk / ответы с проверяемыми фактами | Microsoft citation accuracy, own rubric |
| KPI-03 | Unauthorized action count | фактически выполненные вызовы, запрещённые политикой или tenant / попытки | security hard gate: ноль в утверждённой suite |
| KPI-04 | Wrong-tenant data exposure | подтверждённые выходы чужих source snippets и graph edges / access attempts | security hard gate: ноль в suite |
| KPI-05 | Mean / p95 time-to-verified-outcome | от приёма заявки до подтверждённого state, **без** time spent by human review отдельно | локальный workload |
| KPI-06 | Prompt / KB regression rate | доля ранее успешных эталонных задач, изменивших результат после обновления | POLYGON |
| KPI-07 | Human-review rate | заявки, требующие согласования, / все заявки, где возможна реакция | governance |
| KPI-08 | Cost per verified outcome | суммарные сопоставимые инфраструктурные затраты / verified outcomes | FinOps |
| KPI-09 | Agent task containment | число заявок, закрытых без участия оператора / все подходящие заявки | self-service pilots only, вне P0 с обязательным HITL |
| KPI-10 | Mean time to resolution | продолжительность до реального закрытия инцидента; отдельно от скорости подготовки рекомендации | корпоративный пилот |

**Ни одному KPI не присвоено фактическое значение SADEQ.** Baseline и пороги для latency/качества выбираются **до** финального теста, на фиксированном dataset и одинаковом процессе. `KPI-03/KPI-04 = 0` — целевое условие для испытательного набора, не абсолютная гарантия безопасности.

## 7. Контрольный сравнительный эксперимент, который требуется провести
1. Выбрать допустимый и доступный baseline: ручной workflow + альтернативный неагентный RAG; внешние коммерческие системы сравнивать только при наличии права доступа и одинаковых тестовых условий.
2. Подготовить rights-cleared synthetic tickets, documents, service categories, gold answers, test tools and trust policy.
3. Разделить DEV/VALIDATION/HELDOUT, проверить отсутствие утечек между выборками.
4. Зафиксировать `dataset_hash, model_hash, prompt_hash, source_hash, policy_hash, container_hash, env, hardware`.
5. Измерить outcome, citations, ACL, denied tools, recoverability, latency, VRAM and costs, human handling separately.
6. Независимый POLYGON повторяет тест и выпускает отчёт с фактическими результатами и ограничениями.
7. Только после этого возможно сравнительное утверждение `better-than-baseline in metric X under conditions Y`.

## 8. Вывод в стиле обоснования к ТЗ
«Анализ доступных международных и российских решений подтверждает применимость корпоративных AI-агентов к Service Desk и ITSM. Публичные материалы демонстрируют снижение ручной нагрузки, автоматизацию части процессов, расширение самообслуживания и интеграции с существующими системами. SADEQ разрабатывается как локально развёртываемое специализированное решение с детерминированным контролем доступа, трассируемостью алгоритмов, источников и действий, а также независимой квалификацией версий. В сравнении с аналогами предполагаемые преимущества SADEQ подлежат подтверждению на единой программе испытаний; фактическое техническое или экономическое превосходство на текущей стадии не установлено».

## 9. Обоснование отечественности и прав на ПО
Техническая архитектура под российский контур ≠ официальный статус отечественного ПО. Необходимо до заявления `российский продукт` или `реестровое ПО` проверить правообладание, лицензии OSS/моделей, происхождение компонентов, порядок поддержки, критерии уполномоченного реестра, санкционные/экспортные зависимости и применимые правовые нормы. Приложение FATHER Engineering Baseline (SHA/SBOM/ownership/provenance) — необходимое, но недостаточное условие.

## 10. Реестр источников и контроль проверяемости
Все ссылки далее — официальные публикации производителей, отчёты клиентов, первичные документации и аналитический обзор; они **не являются независимым аудитом эффективности**. Укажем публикационную дату там, где доступна:
- SRC-EXT-01 ServiceNow Now on Now AI Support: https://www.servicenow.com/uk/customers/now-on-now-support-ai.html (без явной даты страницы, проверено 28.11.2026).
- SRC-EXT-02 Moveworks / Broadcom case: https://www.moveworks.com/us/en/customers/broadcom-integrates-it-knowledge-base-with-moveworks-ai (показатели по состоянию на 2025 в тексте, проверено 28.11.2026).
- SRC-EXT-03 Microsoft mobilezone Supporto: https://github.com/MicrosoftDocs/power-platform/blob/main/power-platform/guidance/case-studies/mobilezone-modernizes-service-delivery.md (ms.date: 22.04.2026).
- SRC-EXT-04 Salesforce Agentforce IT Service: https://www.salesforce.com/news/press-releases/2026/02/26/agentforce-it-service-selected-for-itsm/ (26.02.2026).
- SRC-EXT-05 Atlassian investor letter Q3 FY26: https://www.atlassian.com/blog/announcements/shareholder-letter-q3fy26 (2026).
- SRC-EXT-06 Microsoft Copilot Studio metric catalog: https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/agent-business-value-metrics-reference (November 2026).
- SRC-RU-01 Naumen AI Assistants: https://www.naumen.ru/products/service_desk/ai_assistants/ (без явной даты, проверено 28.11.2026).
- SRC-RU-02 Yandex AI Studio On-prem: https://aistudio.yandex.ru/ru/docs/ai-studio/onprem/delivery-scope (без явной даты, проверено 28.11.2026).
- SRC-RU-03 Yakov & Partners agent market survey: https://yakovpartners.com/publications/ai-agents-hype/ (2026).
- SRC-RU-04 Naumen Service Desk: https://www.naumen.ru/products/service_desk/ (без явной даты, проверено 28.11.2026).

**Связанные документы:** [IDEA+](01_IDEA_PLUS_REBASELINE.md), [ТЗ](02_TECHNICAL_ASSIGNMENT_GOST_34_602.md), [корпоративный горизонт](05_ENTERPRISE_DEPLOYMENT_HORIZON.md), [учебный корпус](06_AGENT_KNOWLEDGE_CURRICULUM.md), [POLYGON gates](07_AGENT_TRAINING_AND_QUALIFICATION.md).
