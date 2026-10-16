# FATHER Ecosystem Workspace v0.3

Единый визуальный каркас экосистемы FATHER.

## Модель

### Агенты внутри FATHER
Core-агенты защищены в UI:
- Factory Orchestrator
- Alina Analyst Black Box
- Domain / Action Modeler
- Capability Mapper
- Agent Composer
- Legacy / Project Harvester
- Certification Agent
- Traceability Agent

### Агенты как проекты
Проектные агенты можно расширять и архивировать:
- FATHER OSINT
- FATHER AI-SOC
- SecGraph
- Alina Creative Production
- Avatar Production Agent
- Website Builder & Maintainer
- Game Development Agent
- Prototype Engineering Agent
- Course Harvester / Lesson Agent
- Course Update / Curriculum Agent
- DevOps
- DevSecOps
- Platform / Kubernetes
- Security Architect
- Compliance
- QA / AI Eval
- Observability / SRE

### Стандартная внутренняя структура агента
- Identity / Passport
- Prompt / Policy
- Knowledge Base
- RAG / Retrieval
- Databases / State
- Memory
- Tools / MCP / API
- Workflow / Graph
- Security / Guardrails
- Tests / Eval
- Observability
- Deployment / Runtime
- Documentation
- Evidence / History

### Интеграционные запчасти
В registry включены OpenAI/GPT, Google Gemini/Vertex AI, Drive/Docs, Sheets, Gmail,
Calendar, YouTube, GCP, Azure/OpenAI, GitHub, GitLab, Anthropic, Ollama,
PostgreSQL/pgvector, Neo4j и MCP.

Интеграционный слой хранит только паспорт/контракт. Credentials и secrets не хранятся в визуальном registry.

## Запуск

```powershell
cd "G:\1\OTUS"
git fetch origin
git switch feature/father-ecosystem-workspace-v03
git pull
python -m http.server 8088
```

Открыть:

`http://localhost:8088/factory/ecosystem-v03/`

## Правило Алины

Alina Analyst в этом workspace — black box. Внутренняя реализация ведётся отдельно; сюда подключается её внешний контракт.
