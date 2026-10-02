# Professional Security Learning Registry

Назначение: отдельный реестр внешнего профессионального обучения по информационной безопасности. Он не смешивается с `COURSE_REGISTRY.yaml`, который описывает учебный поток OTUS AI Architect.

## Статусы

- `IN_PROGRESS` — обучение проходит сейчас / заявлено как текущее.
- `COMPLETED` — завершено и есть подтверждение.
- `VERIFY` — нужно отдельно подтвердить код программы, даты или документ.

## Текущие направления

| ID | Направление | Провайдер | Статус | Evidence | Как использовать в резюме |
|---|---|---|---|---|---|
| SEC-LEARN-001 | Security Engineer / Инженер по информационной безопасности | CyberED | IN_PROGRESS | VERIFY | «Прохожу углублённое обучение по Security Engineering»; не указывать как завершённую квалификацию до документа |
| SEC-LEARN-002 | Penetration Tester / Пентестер | CyberED | IN_PROGRESS | VERIFY | «Прохожу практический трек по penetration testing / offensive security»; навыки переносить в CV только по фактически выполненным labs |
| SEC-LEARN-003 | SOC Analyst / Аналитик SOC | CyberED | IN_PROGRESS | VERIFY | «Прохожу обучение по SOC / мониторингу и анализу событий ИБ»; SIEM/SOC hands-on заявлять по подтверждённым лабораториям |

## Известные коды программ

- Security Engineer — ранее в материалах фигурировал код `F-402`; подтвердить актуальность перед публичным использованием.
- Penetration Tester — ранее в материалах фигурировал код `R301`; подтвердить актуальность перед публичным использованием.
- SOC Analyst — точный код программы в текущем реестре не зафиксирован; не придумывать.

## Правило для MASTER CV

Пока обучение не завершено:

`Дополнительное образование / обучение — Security Engineer, Penetration Testing, SOC Analysis (в процессе)`

После завершения каждого трека добавляем:

`дата → точное название → провайдер → часы → документ/сертификат → ключевые labs → evidence links`

## Связь с компетенциями

- Security Engineer → Security Architecture, IAM/RBAC, network/security controls, vulnerability management, endpoint/network protection.
- Penetration Tester → recon, web security, auth attacks, Linux/Windows privilege escalation, network/AD labs, reporting.
- SOC Analyst → SIEM, telemetry, detection, triage, incident analysis, playbooks, escalation, reporting.

Обучение само по себе не подменяет WORK experience. Для резюме используются отдельно `WORK`, `PROJECT`, `LAB`, `KNOWLEDGE`, `VERIFY`.