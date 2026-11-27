# ECON-CLOUD-2026-11-27 · Реальные тарифы РФ, 3 размещения и модель TCO
**Статус:** PRICES_VERIFIED_FROM_PROVIDER_PUBLIC_PAGES / AVAILABILITY_UNKNOWN / CUSTOMER_QUOTE_REQUIRED.  
**Дата чтения:** 27 ноября 2026 · **Валюта:** ₽, с НДС по опубликованным источникам · **Срок действия:** перепроверить перед закупкой и защитой.

## Решение о границе системы
**FINAL OTUS MVP: полностью on-prem / air-gapped**, не может обращаться к публичному облаку, внешним inference API, облачным управляемым БД или OSS SaaS. Данные, образы, модели и SBOM заносятся через отдельную контролируемую процедуру. Облако здесь — только **экономическое сравнение альтернативных поставок для заказчика**, не способ обойти air-gap.
Рассматриваем три решения:
- **A — Local LAB:** уже имеющаяся RTX 3060 12GB, Windows/WSL2, локальная Qwen квантованная, контейнеры, без SLA.
- **B — Private On-Prem:** Linux GPU server(s), отдельные DB/backup/monitoring и управление секретами, реальная изолированная сеть.
- **C — Cloud IaaS / isolated private cloud:** self-hosted models на арендуемом GPU, приватные сегменты и VPN/Direct Connect; **не air-gapped** по умолчанию. Действует только при изменении требования заказчика и отдельном правовом/ИБ заключении.
- **D — Hybrid with cloud:** контрольный план/данные local и вычисление cloud; ***не проходит strict air-gap***, только будущая опция для другой политики данных.

## Сверенные тарифные позиции (источники провайдеров)
| ID | Сервис/конфигурация | ₽/час, НДС включён | 40 часов/мес | 160 часов/мес | 730 часов/мес | Scope |
|---|---|---:|---:|---:|---:|---|
| PR-01 | Cloud.ru Evolution Compute: Intel Xeon Platinum / **2x A100 80GB NVLink**, 30 vCPU, 228GB RAM | 732.00 | 29 280 | 117 120 | 534 360 | VM, storage/network/backups separate |
| PR-02 | Cloud.ru Evolution Compute: Intel Xeon Platinum / **4x A100 80GB NVLink**, 60 vCPU, 456GB RAM | 1 464.00 | 58 560 | 234 240 | 1 068 720 | VM, storage/network/backups separate |
| PR-03 | Yandex DataSphere config **g2.1: 1x A100**, 28 vCPU | 542.88 | 21 715.20 | 86 860.80 | 396 302.40 | DataSphere job/notebook/inference configured compute |
| PR-04 | Yandex DataSphere config **g1.1: 1x V100**, 8 vCPU | 336.96 | 13 478.40 | 53 913.60 | 245 980.80 | DataSphere configured compute |
| PR-05 | Yandex DataSphere config **gt4.1: 1x T4**, 4 vCPU | 168.48 | 6 739.20 | 26 956.80 | 122 990.40 | DataSphere configured compute |
| PR-06 | Yandex DataSphere config **c1.4: 4 vCPU, no GPU** | 18.72 | 748.80 | 2 995.20 | 13 665.60 | compute for separate workload, not an LLM GPU |
| PR-07 | Yandex DataSphere storage (beyond initial free 10GB): 1GB-month | 12.90/GB-month | formula | formula | formula | storage only |

**Прямые первоисточники:**
- Cloud.ru 2x/4x A100: https://cloud.ru/documents/tariffs/evolution/evolution-compute-gpu — **версия 260909, действует с 9 сентября 2026**, строка 5 и строка 6 таблицы для Intel Xeon; опубликованный НДС 22%.
- Yandex DataSphere: https://yandex.cloud/ru/docs/datasphere/pricing — раздел «Цены для региона Россия», g2.1/g1.1/gt4.1/c1.4, storage; цены ₽/час, включая НДС.
- Yandex Compute: https://yandex.cloud/ru/docs/compute/pricing — **не приравнивать** стоимость Compute GPU к DataSphere; цена VM зависит от vCPU, RAM, GPU, диска, ОС, IP и outbound; региональные цены различаются.
- Selectel Cloud GPU: https://selectel.ru/services/cloud/servers/gpu/ — динамический конфигуратор, цены зависит от региона/пула; в статическом отображении **точная ставка за выбранный GPU не фиксируется надёжно**, поэтому в этом документе ставка Selectel = `TO_QUOTE`. Дополнительный внешний трафик указан **0,90 ₽/GB после бесплатных 3 TB** на публичной странице (действуют условия тарифа); пул/наличие нужно подтвердить.
- Selectel регион и доступность, например Санкт-Петербург / ru-9a — подтверждать в калькуляторе до оплаты.

### Важные ограничения сравнения тарифов
1. Cloud.ru Compute и Yandex DataSphere — **разные продукты**, разные составы конфигураций; нельзя вычитать 732−542.88 и объявлять «один провайдер дороже на 189,12» за одинаковый ресурс.
2. Опубликованная ставка GPU не является полной стоимостью 24/7 системы SADEQ: добавляются storage, snapshots, DB/HA, monitoring, сеть, backup, ingress/egress, лицензии, инженерный труд.
3. Если арендована невыделенная конфигурация, нужно проверить гарантии доступа к GPU/изоляцию. Наличие A100 в прайсе ≠ доступная квота.
4. У Yandex DataSphere цены для региона Россия; у Cloud.ru уточнить зону размещения, контракт и условия доступа.
5. «Реальная цена» = публично опубликованный тариф на дату анализа, **не принятая коммерческая оферта**. Скидки и квоты неизвестны.

## Сценарии нагрузки и оплаты
`GPU_compute_cost = hourly_tariff × actual_billable_hours`.  
`MONTHLY_TCO = GPU + CPU_workers + DB + SSD/S3 + Snapshots + Network/VPN/Egress + Logs + Backups + Secrets + Operations + Security + Amortization + Contingency`.

- **40 ч/месяц:** демонстрации/нагрузочные эксперименты, ресурс выключен между сессиями; оплачиваемые диски могут продолжать тарифицироваться.
- **160 ч/месяц:** рабочее время с операторским запуском; не обеспечивает 24/7 SLA.
- **730 ч/месяц:** круглосуточное использование 365*24/12 ≈730; HA требует дополнительных экземпляров и failure domains, а не только увеличение числа часов.
- **10k RPS:** разделять caching/API read, retrieval-only, full GenAI completion. Формула GPU sizing: `required_GPU = ceil(peak_generated_tokens_per_sec / measured_tokens_per_sec_per_GPU / target_utilization)` после учёта TTFT, concurrency, batch, per-request context length. Это первичная оценка, а не проверенная пропускная способность.

## Пороговый анализ Local / On-Prem vs GPU cloud
**Купленная GPU-машина:** 
`TCO_local_month = (GPU_server_CAPEX - residual_value)/life_months + electricity_kWh*tariff + cooling + labor + backup + maintenance + spare_capacity + downtime_risk`. 
Пример **нефактической сметы**: сервер за 600 000 ₽, срок 36 мес, остаточная стоимость 0, power+cooling 4 000 ₽/мес, maintenance+support 5 000 ₽/мес → **25 666.67 ₽/мес**, без администратора и других серверов. Эта цифра НЕ является предложением продавца.
Сравнивать с PR-03 (A100) напрямую нельзя: у примера нет подтверждённой эквивалентной GPU производительности. Сравнение корректно только после **равного workload/quality/SLO** и учёта полноценного stack.

## Рекомендованная политика запуска ресурсов
- Для **LAB:** существующее железо, нулевые дополнительные закупки до теста VRAM/throughput; считать opportunity cost и электричество.
- Для **пилота:** доступный Linux VM / узел с ограничением расхода; не оплачивать GPU 730 часов, если запросы идут 40 часов.
- Для **регулируемой эксплуатации:** private on-prem с резервированием и offline update channel при жёстком требовании air-gap.
- Для **нестрогого enterprise use:** сравнить private cloud GPU IaaS и on-prem; записать юридический risk acceptance, сетевые boundaries, SLA и расчёт 3-летнего TCO.

## Сценарная чувствительность
Для каждого варианта LOW/BASE/HIGH: часы/месяц 40/160/730, concurrency, index GB, storage retention, token volumes, p95 SLO, backtracking rate, rejected results, standby GPU nodes 0/1/2. Тест +50% GPU ставки, +50% token demand, падение quality 10%, increase human review. Чувствительность и график break-even должны жить в spreadsheet с формулами, а не в процентах из головы.

## Cost metrics
- `cost_per_qualified_outcome = monthly_TCO / independently_accepted_outcomes`; denominator 0 → undefined.
- `agent_specialization_cost = ontology + source ingestion + algorithm adapter + approval flow + tests + ongoing requalification`.
- `unit_economics=price_per_accepted_result - fully_allocated_cost_per_accepted_result`.
- **FinOps stop:** spending cap / idle GPU alert / review when queue/SLO changes. Нет права обходить air-gap через облако при budget breach.

## ADR-cloud-001 (проектное)
**Decision:** Final OTUS deployment = air-gapped local; public cloud is a non-deployed commercial alternative only.  
**Rationale:** explicit acceptance requirement; fewer network/data exposure pathways.  
**Costs:** hardware CAPEX and offline supply-chain operations; less elasticity than cloud.  
**Review:** при изменении условий заказчика и наличии технических/юридических подтверждений.

## Источники и протокол обновления
Тарифы записаны с URL и датой анализа. Для Selectel динамическую ставку НЕ выдаём за зафиксированный факт. Перед защитой/коммерческим КП повторно собираем тарифы, регион, VAT, GPU SKU, возможность аренды, стоимость дисков/сети, квоты и условия договора. Любое изменение тарифа отражать новой версией с retrieval timestamp.
