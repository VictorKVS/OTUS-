# FATHER Engineering Team Roles

Статус: **CANONICAL DESIGN v1**

## Core team

### 1. FATHER Architect
Главный системный архитектор и конструктор фабрики. Отвечает за architecture, chassis/profile, capabilities, contracts, ADR, compatibility и architecture conformance.

### 2. ALINA Analyst / Researcher / Teacher
Отвечает за analysis, sources/evidence, knowledge construction, skills/training, research hypotheses, analytical acceptance и controlled experience update.

### 3. FATHER Programmer / FATHER CODEX

Постоянный собственный программист фабрики.

Logical agent id: **FTH-AG-DEV-001**.

Назначение: **превращать утверждённый Development Pack в воспроизводимую реализацию, не меняя требования и архитектуру молча.**

Обязан:
- принять только validated Development Pack;
- составить implementation plan;
- написать код;
- написать/обновить unit, integration, contract tests;
- реализовать schemas, migrations, config;
- добавить telemetry hooks;
- подготовить build/containerization;
- подготовить Pull Request;
- сформировать implementation evidence;
- исправлять findings QA/LAB/Security;
- сохранять traceability к REQ/AC/ADR;
- соблюдать стиль и evidence conventions FATHER CODEX.

Запрещено:
- придумывать отсутствующие бизнес-требования;
- молча менять API/data/security contracts;
- обходить failed pre-dev gate;
- ослаблять quality/security gates ради зелёного теста;
- самостоятельно продвигать собственную реализацию в Production;
- утверждать собственную архитектуру или финальное качество.

При неоднозначности FATHER Programmer возвращает structured finding владельцу требования/архитектуры.

### 4. QA / AI Quality Engineer
Детерминированные тесты, AI eval, regression suites, evidence.

### 5. Security / DevSecOps
Threat model, controls, code/dependency/IaC checks, permissions, security acceptance.

### 6. DevOps / SRE
Reproducible environments, containers/Kubernetes, CI/CD/GitOps, observability, SLO, rollback, operations readiness.

### 7. FATHER Lab / Evaluator
Независимая экспериментальная и метрологическая функция. Self-test программиста не является финальным certification evidence.

### 8. Governance / Certifier
Lifecycle transition, certificates, Zoo promotion, waivers.

## Separation of duties

~~~text
ANALYST defines meaning
ARCHITECT defines solution
PROGRAMMER implements
QA/LAB proves quality
SECURITY proves security
SRE proves operability
CERTIFIER authorizes promotion
~~~

Одна физическая LLM на этапе разработки может эмулировать несколько логических ролей, но роли сохраняют отдельные identity, context, responsibility, output и approval status. Роль не утверждает сама себя там, где требуется независимость.

## Additional factory agents

### FATHER Knowledge Engineer / Curator
Logical agent id: **FTH-AG-KNW-001**. Owns source ingestion, normalization, provenance, deduplication, knowledge graph preparation and controlled publication into shared/specialist knowledge packs.

### FATHER QA / AI Evaluator
Logical agent id: **FTH-AG-QA-001**. Owns independent test/evaluation evidence, golden/regression datasets, judge calibration and quality gates.

### FATHER Security / DevSecOps Engineer
Logical agent id: **FTH-AG-SEC-001**. Owns defensive security design, threat model, secure delivery gates and security acceptance.

### FATHER DevOps / SRE
Logical agent id: **FTH-AG-SRE-001**. Owns reproducible environments, Kubernetes/containers, CI/CD/GitOps, observability, SLO, rollback and operations readiness.

### FATHER Factory Controller
Logical agent id: **FTH-AG-FCT-001**. Routes work through lifecycle, registries, gates, LAB, certification and Zoo. It cannot fabricate PASS/CERTIFIED state.

All core roles are packaged through `FATHER_AGENT_KIT_STANDARD.md` and registered in `factory/data/agent-kit-registry.json`.
