# Security Requirements, Compliance & Architecture Interview Playbook

## Requirements engineering

Сквозная цепочка: `Source → Requirement → Applicability → Gap → Control → Architecture/Process → Task → Test → Evidence`.

Collection: законы/регуляторика, стандарты, договоры, internal policies, business requirements, architecture/NFR и security requirements.

Decomposition: большое требование разбивается на атомарные `REQ-xxx`, чтобы его можно было назначить, реализовать и проверить.

Applicability: для каждой нормы определить систему, данные, процесс, роли и условия применимости.

Gap analysis: `As-Is vs Required State → Gap → Remediation`.

Control mapping: `REQ → Control → Component/Process → Owner → Test → Evidence`.

Traceability должна работать в обе стороны — от источника до evidence и от технической меры до основания.

## Security architecture discovery

`Business processes → Data → Systems/assets → Owners/users → Data flows → Regulatory scope → Threats/risks → Access → Controls → Monitoring → Recovery → Evidence`.

## Access governance

RBAC, least privilege, need-to-know, segregation of duties, privileged access, access matrix, joiner/mover/leaver lifecycle. Важно знать не только кто получает доступ, но и кто его утверждает и как он отзывается.

## Segmentation

Разделять trust zones: user, server, admin, security, backup, regulated/special systems, external/DMZ when applicable. Цель — контролировать flows и уменьшать blast radius.

## Backup & Recovery

RPO, RTO, 3-2-1, offline/immutable copy, encryption, retention, restore test. Backup считается рабочим только когда восстановление регулярно проверяется.

## DLP / SIEM / EDR / WAF

DLP — контроль движения защищаемой информации и пользовательских каналов. SIEM — централизация/корреляция событий и detection. EDR — endpoint telemetry, behavioral detection, containment/response. WAF — контроль web traffic перед приложением. DLP не является основным средством обнаружения внешнего вторжения.

## Vulnerability vs Risk Management

Vulnerability management: `Discover → Validate → Prioritize → Remediate/Compensate → Retest → Close`.

Risk management: `Asset + Threat + Weakness + Likelihood + Impact → Risk → Treatment`.

Treatment: reduce, avoid, transfer, accept. Risk-based vulnerability management учитывает не только CVSS, но и критичность актива, exposure, exploitability и последствия.

## Regulated environments

В резюме: «практическое понимание и опыт работы с требованиями ИСПДн, ГИС, КИИ и организационно-техническими мерами защиты». Не заявлять экспертность по каждому нормативному документу без подтверждаемого опыта.

## Контрольные вопросы

1. С чего начать ИБ в организации с низкой зрелостью?
2. Requirement vs control?
3. Что такое applicability?
4. Как построить access matrix?
5. Почему backup на соседнем сервере может не спасти?
6. DLP vs SIEM?
7. Почему CVSS 9.8 не всегда чинится первым?
8. Что делать с legacy system, которую нельзя обновить?
9. Как доказать выполнение требования?
10. Как связать compliance с архитектурной разработкой?