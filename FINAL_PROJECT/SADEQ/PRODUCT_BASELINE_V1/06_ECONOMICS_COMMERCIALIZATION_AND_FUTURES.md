# FIN-ROADMAP-001 — Экономика, коммерческое внедрение и перспективы
**Версия 1.0 · расчётные гипотезы отделены от верифицированных тарифов.**

## Целевые варианты и экономическое решение
LOCAL desktop: lowest incremental equipment CAPEX for course demo, but single-machine bottleneck and no guaranteed SLA.  
PRIVATE ON-PREM: purchase GPU and backup capacity, long amortization; best when strict airgap, predictable load, strong data control.  
CLOUD IaaS: tariff pay-per-hour, rapid experiments and time-bounded burst; **not air-gapped**, business/legal change required.  
HYBRID: controlled future option, more integration/security overhead.

## Тарифы, дата, методика
[Прайс-реестр на 27 ноября 2026](../IDEA_PLUS_V0_2/11_DEPLOYMENT_CLOUD_FINOPS_RU_2026.md) с прямыми URL и НДС; например Cloud.ru 2×A100 VM 732 ₽/час, Yandex DataSphere g2.1 A100 542,88 ₽/час — **разные продукты и комплектации**, прямое price/GPU сравнение некорректно. 40/160/730 часов работы вычисляются отдельно. Диски, BaaS, egress, load balancers, snapshots, network, supporting CPU workers, taxes, discounts and SLA exclude from headline price; include in TCO.

## TCO 3 года
`TCO_36 = CAPEX - residual_value + 36 * (power + cooling + maintenance + operators + security + backup + licenses + logs + networking + compliance) + planned_refresh`.
`TCO_cloud_36 = GPU_hours * hourly_tariff + DB + storage + network + backup + monitoring + operations + HA reserve + tax_adjustments`.
`cost_accepted = total_cost_of_all_attempts / independently_accepted_outcomes`.
Провести LOW/BASE/HIGH, скидка и +50% цены, 2× нагрузка, сценарий 1 GPU / 2 GPU / cluster, отдельные затраты аттестации 3/20 профилей.

## Агентная фабрика: break-even как предположение
Демонстрационный сценарий, не смета: shared engineering 600 ч; самостоятельный агент 200 ч; специализация 40 ч; breakeven ceil(600/(200−40))=4. При 20: 1 400 vs 4 000 ч; экономия **только при равных функциях и квалификации**, без инфраструктуры/сопровождения. В жизненном цикле квалификации разных доменов выгода может исчезнуть.

## Варианты коммерческой модели
1. Annual enterprise licence + on-prem installation;
2. Per-qualified-domain-pack support contract;
3. Paid integration and migration;
4. Support tier with defined response times;
5. OEM/SDK licensing to integrators (legal review).
Не фиксировать тариф продажи до реального customer discovery, себестоимости и коммерческих ограничений.

## Стратегическая перспектива по триггерам
**0–6 месяцев как ориентир, не срок:** доказать POC и принятый MVP; 3 профиля, QA bench, локальность.  
**6–18 месяцев условно:** клиентский пилот, Kubernetes только при требуемом масштабе, SLA, multi-tenancy после ACL tests.  
**18–36 месяцев условно:** marketplace доменных профилей, agent registry, qualified skill pack contracts, multi-site deployment, private cloud SKU, continuous independent qualification, доказанная экономика.
Не обещать календарные даты, если нет бюджета/команды/подтверждённого спроса.

## Риски коммерциализации
Гибридная обработка конфиденциальных данных, vendor licensing, высокие расходы экспертной проверки, постоянная поддержка, интеграция ERP/МИС, model drift, customer trust, конкурирующие платформы. Бизнес-кейс требует интервью, пилота и данных эксплуатации.

## Commercial Go / No-Go
**GO:** принят пилот, подтверждён спрос, лицензии и security, измерены cost/accepted outcome, повторяемость и SLO, имеются support и deployment runbooks. Иначе RESEARCH/NO GO.
