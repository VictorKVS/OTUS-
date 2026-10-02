# FATHER Architect OS — OTUS Architecture Cockpit

Статический сайт-витрина сквозного проекта курса «Архитектор AI-систем».

## Зачем

Сайт не заменяет артефакты уроков. Он связывает их в одну проверяемую архитектурную историю:

`BUS → REQ/NFR → RISK → ADR → CMP → CTRL → TEST → SLO → COST → REL`

Источник истины — файлы и тестовые артефакты в Git. Если подтверждающего артефакта нет, сайт не должен помечать урок как готовый.

## Что уже показывает

- 31 урок курса;
- 7 контрольных gates;
- доказательные статусы `ГОТОВО / REVIEW / DRAFT / LAB / МАТЕРИАЛЫ`;
- ссылки на реальные папки уроков в GitHub;
- ADR/TCO/CTO Challenge по хостингу LLM;
- сквозную traceability chain;
- классы evidence: документы, код, тесты, эксплуатационные метрики;
- светлую/тёмную тему и фильтр уроков.

## Модель статусов

Статус не равен проценту готовности:

- `done` — есть завершённый и принятый/merged артефакт;
- `review` — результат подготовлен и находится на review;
- `draft` — есть проверяемый draft, но gate не закрыт;
- `lab` — есть рабочий технический контур/лабораторная реализация;
- `materials` — в репозитории есть материалы урока, но завершение результата не подтверждено.

## Локальный запуск

Из `G:\1\OTUS`:

```powershell
cd site
py -m http.server 8088
```

Открыть:

```text
http://127.0.0.1:8088/
```

Сайт не требует npm, Node.js, внешних CDN или API.

## Правило развития по каждому следующему уроку

1. сохранить исходное задание/материалы;
2. создать проверяемый артефакт урока;
3. связать его с существующими BUS/REQ/NFR/RISK/ADR/CMP/CTRL/TEST/SLO/COST/REL;
4. добавить тест/метрику/ревью, где это требуется;
5. только после evidence обновить статус в `site/app.js`;
6. не переписывать принятые ADR: новое решение оформляется через новый ADR/supersede;
7. не использовать учебные TCO-цифры как текущий рыночный прайс без актуализации источников и допущений.

## Ближайшие доработки

- вынести реестр уроков из `app.js` в машинно-читаемый manifest;
- автоматически собирать статусы из merged/open PR и CI evidence;
- добавить страницы Gate/ADR/Architecture Pack;
- добавить C4/DFD/BPMN/OpenAPI preview;
- добавить матрицу `requirement → decision → component → test`;
- добавить quality/SLO/FinOps dashboards по мере появления измерений;
- подготовить безопасную публикацию через GitHub Pages или отдельный static hosting после review.


## Visual-first engineering standard

Для каждой темы, урока и capability действует единый порядок:

`Schema → Visual → Meaning → Artifacts → Evidence → FATHER Mapping → Maturity`

Каждая страница должна показывать три слоя:

1. **OTUS Curriculum** — исходная программа и требования урока.
2. **Architect Pro** — профессиональная методика, trade-offs, стандарты и инструменты.
3. **FATHER Production** — рабочий компонент/контур боевой платформы.

Нотация, maturity levels и capability vocabulary закреплены в:
[`docs/STEP_00_NOTATION_AND_VISUAL_LANGUAGE.md`](../docs/STEP_00_NOTATION_AND_VISUAL_LANGUAGE.md).

Пошаговый план:
[`docs/FATHER_ARCHITECT_OS_BUILD_PLAN.md`](../docs/FATHER_ARCHITECT_OS_BUILD_PLAN.md).

Дневник:
[`docs/DEVELOPMENT_JOURNAL.md`](../docs/DEVELOPMENT_JOURNAL.md).


## STEP 01 — Master Architecture Map

Готова первая production-oriented master map:

- [Master Architecture Map](./step-01-master-map.html)
- [Capability manifest](./data/capabilities.json)
- [SVG poster](./assets/step-01-master-architecture.svg)

STEP 01 связывает OTUS Curriculum → Architect Pro → FATHER Production и вводит постоянные component IDs.


## STEP 02–04

- [STEP 02 · Course Manifest](./step-02-course-manifest.html)
- [STEP 03 · Universal Lesson Template](./step-03-lesson-template.html)
- [Lesson 01 · normalized view](./lesson-template.html?id=1)

Lesson 01 теперь служит эталоном: schema + visual + OTUS + Architect Pro + FATHER Production + evidence + maturity.


## Lesson 02 normalized

- [Lesson 02 · Estimation / Risk / Cost](./lesson-template.html?id=2)
- visual: `assets/lesson-02-estimation-risk-cost.svg`
- data: `data/lesson-details/02.json`

Production mapping: Requirements → Estimation/Planning → Risk/Change Control → FinOps.


## Lesson 03 normalized

- [Lesson 03 · PoC → Production](./lesson-template.html?id=3)
- visual: `assets/lesson-03-poc-to-production.svg`
- data: `data/lesson-details/03.json`

Production mapping: Value Delivery / Stage Gates → Estimation → Risk/Change → FinOps → Delivery.


## Lesson 04 normalized

- [Lesson 04 · HLD / C4](./lesson-template.html?id=4)
- visual: `assets/lesson-04-hld-c4.svg`
- data: `data/lesson-details/04.json`

OTUS C1/C2 отделены от существующего Architect Pro extension: C3 + Deployment + richer AI roles.


## Lesson 05 normalized

- [Lesson 05 · LLD / Components / Contracts](./lesson-template.html?id=5)
- visual: `assets/lesson-05-lld-contracts.svg`
- data: `data/lesson-details/05.json`

Completed evidence package: C2 → C3 → Sequence → OpenAPI → CI/evidence.


## Lesson 06 normalized

- [Lesson 06 · RAG Patterns](./lesson-template.html?id=6)
- visual: `assets/lesson-06-rag-patterns.svg`
- data: `data/lesson-details/06.json`

Notebook evidence: vector retrieval + BM25 hybrid + reranking code; no saved execution outputs, so status remains `draft / M1`.


## Lesson 07 normalized

- [Lesson 07 · AI Agents & Multi-Agent](./lesson-template.html?id=7)
- visual: `assets/lesson-07-multi-agent.svg`
- data: `data/lesson-details/07.json`

M1.1 evidence includes LangGraph typed state, explicit handoffs, Hybrid RAG, tests and CI workflow definition.

### Status semantics update

Lesson pages now show two independent states:

- engineering status / maturity;
- OTUS course submission status.

A completed Git artifact is not automatically treated as teacher acceptance.


## Lesson 08 normalized

- [Lesson 08 · Architecture Decision Records](./lesson-template.html?id=8)
- visual: `assets/lesson-08-adr-lifecycle.svg`
- data: `data/lesson-details/08.json`

Decision lifecycle: context → options → trade-offs → review → accepted → fitness evidence → review trigger → supersede.


## Lesson 09 normalized

- [Lesson 09 · Architecture Verification / CTO Challenge](./lesson-template.html?id=9)
- visual: `assets/lesson-09-architecture-verification.svg`
- data: `data/lesson-details/09.json`

Engineering status remains `review / M1`: challenge preparation exists, but a completed ATAM/CTO review session is not evidenced.


## Lesson 10 normalized

- [Lesson 10 · Architecture Governance / Technical Debt](./lesson-template.html?id=10)
- visual: `assets/lesson-10-governance-tech-debt.svg`
- data: `data/lesson-details/10.json`

Source evidence is limited to lesson material, so engineering status remains `materials / M0`.

## Milestone: Lessons 01–10

The first ten lessons now use one visual-first contract:

`Schema → Visual → OTUS Curriculum → Architect Pro → FATHER Production → Artifacts/Evidence → Traceability → Maturity`.


## Lesson 11 normalized

- [Lesson 11 · Integrations from classic to AI standards](./lesson-template.html?id=11)
- visual: `assets/lesson-11-integrations-ai-standards.svg`
- data: `data/lesson-details/11.json`

Production mapping: Contract Registry → Integration Runtime/Messaging → MCP/AI Gateway → Security/Observability.


## Lesson 15 normalized — Observability

- [Lesson 15 · AI Observability](./lesson-template.html?id=15)
- visual: `assets/lesson-15-observability-ai.svg`
- data: `data/lesson-details/15.json`

Engineering status: `LAB / M1`. Course submission status remains `not submitted`.

Production chain:

`Observability → SLO/Alerting → Eval/Security/FinOps → Runbook → Incident/RCA → Change`.


## Lesson 16 normalized — Sizing / Capacity

- [Lesson 16 · Resource Sizing](./lesson-template.html?id=16)
- visual: `assets/lesson-16-sizing-capacity.svg`
- data: `data/lesson-details/16.json`

Engineering status: `draft / M1`.

Sizing chain:

`SLO → Workload → CPU/RAM/GPU/Storage → Replicas/Headroom → Benchmark → On-prem/Cloud → TCO → Capacity Gate`.

Agent production standard:

- [AGENT_PRODUCTION_STANDARD.md](../docs/AGENT_PRODUCTION_STANDARD.md)

Каждый production-agent теперь обязан иметь workload profile, sizing assumptions, benchmark/capacity evidence и cost budget.


## Lesson 17 normalized — LLM Inference

- [Lesson 17 · LLM Inference Sizing](./lesson-template.html?id=17)
- visual: `assets/lesson-17-llm-inference-optimization.svg`
- data: `data/lesson-details/17.json`
- homework report: `../17. Расчёт ресурсов и оптимизация инференса LLM  ДЗ/DZ_17_SIZING_REPORT.md`

Engineering status: `draft / M1`.

Inference chain:

`Model/SLO → VRAM → Quantization → Engine/Batching → Benchmark → GPU placement → Cost → Inference Gate`.

The homework calculation is ready as XLSX + native Google Sheet; course submission is still separate.


## FATHER Document Conveyor

Добавлен канонический end-to-end маршрут проектной документации:

- [Document Conveyor](./document-conveyor.html)
- data contract: `data/document-conveyor.json`
- visual: `assets/father-document-conveyor.svg`
- engineering document: `../docs/FATHER_DOCUMENT_CONVEYOR.md`

Главный handoff:

`RAW INPUT → INTAKE PACK → ANALYSIS PACK → ANALYST/ARCHITECT HANDSHAKE → ARCHITECTURE PACK → CROSS-CUTTING GATES → DEVELOPMENT PACK → DEVELOPER → CI/QA → ANALYST ACCEPTANCE → ARCHITECT ACCEPTANCE → RELEASE`.

Перед программистом обязательны два независимых sign-off:
1. аналитик подтверждает смысл/полноту/acceptance criteria;
2. архитектор подтверждает реализуемость/NFR/interfaces/ADR.

Программист получает task-scoped Development Pack, а не сырой архив проекта.
