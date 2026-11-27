# SADEQ-ACC-001 — Независимая верификация, выпуск и передача
## Четыре независимых вида проверки
1. **Document completeness:** все обязательные по ТЗ типы документов есть в ведомости, имеются согласования, коды/версии, правильное оформление в выбранном стандарте.
2. **Engineering consistency:** FR/NFR, C4, BPMN, ALG, API, DATA, THR, TEST взаимно согласованы; нет неучтённых потоков или дублирующих владельцев.
3. **Implementation qualification:** действительный код/модели/образ/конфигурация в целевом окружении прошли реальные negative/integration/performance/restore tests; POLYGON сохраняет EVI по exact hash.
4. **Formal acceptance:** уполномоченная сторона рассматривает документы, результаты, замечания, результаты предварительных испытаний и опытной эксплуатации и принимает решение по договору. Ни GitHub, ни POLYGON не подменяют заказчика.

## Процедура приемки комплекта
`Freeze baseline → verify document manifest → verify applicability of standards → audit requirements mapping → inspect sensitive data classification → validate diagrams/schemas → verify commits and signatures → execute tests → independent review → issue defect list → remediate and rerun → human signoff → immutable release archive`.

## Доказательства
Ведомость EVI должна включать: документ, источник, hash, обязательность, выпущенный формат, подписанта; для тестов: test ID, утверждённую версию ПМИ, environment, image digest, config digest, model hash, executed_at, observed result, log/dataset hash, examiner decision.

## Формальные статусы
`DRAFT → FOR_REVIEW → REVIEWED → APPROVED_DOC`, далее **отдельно** `IMPLEMENTED → TESTED → QUALIFIED → ACCEPTED`. Допустимы `RETURNED_FOR_CORRECTION`, `BLOCKED`, `REVOKED`.
- Полный комплект с черновиками нельзя объявлять `APPROVED_DOC`.
- Прохождение unit tests не означает приёмку АС.
- Некритичные замечания закрываются решением уполномоченной комиссии в пределах утверждённых критериев; угрозы, запрещающие эксплуатацию, не принимаются по произвольному исключению.
- При замене версии/алгоритма/модели/политики документ и квалификация анализируются заново.

## Формальный выпуск
Сформировать выдаваемый архив `manifest + DOCS + CODE/SBOM + TESTS + EVIDENCE + APPROVAL`. Публичный investor deck хранить отдельно, любые claims проверять по EVI; специальные закрытые исходники и реквизиты военного заказа не публиковать.

## Что реально нужно выполнить далее
- согласовать официальный состав, применимость ГОСТ и обозначения с владельцем SADEQ/условным заказчиком;
- подготовить рабочее ТЗ по разделам ГОСТ 34.602;
- оформить ЭП по B01..B08, затем ТП/LLD по ALG-01..12;
- подготовить 12 отдельных схем ГОСТ 19.701 и ПМИ;
- провести тесты и подписать протоколы по реально собранному и развёрнутому изделию.

**Текущий статус:** регламент и план; реальная военная приёмка, сертификаты, утверждённые ГОСТ-формы и POLYGON evidence отсутствуют.
