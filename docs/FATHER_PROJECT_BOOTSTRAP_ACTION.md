# FATHER Project Bootstrap Action

Статус: **CANONICAL ACTION TEMPLATE v1**

Назначение: единый порядок создания любого нового проекта FATHER локально и на GitHub.

## A00–A12

| Step | Action | Gate |
|---|---|---|
| A00 | Зафиксировать PROJECT_NAME / PROJECT_ID / owner / purpose | name_unique |
| A01 | Создать локальный корень `G:\\1\\<PROJECT_NAME>` | local_root_exists |
| A02 | Развернуть стандартный каркас проекта и C00–C99 dossier | template_created |
| A03 | Создать `README.md`, `.gitignore`, `.env.example` | baseline_files_exist |
| A04 | Инициализировать Git: `git init -b main` | git_repo_ok |
| A05 | Выполнить secret pre-check до первого commit | no_secrets |
| A06 | Первый commit `chore: bootstrap <PROJECT_NAME>` | baseline_commit |
| A07 | Создать private GitHub repo `VictorKVS/<PROJECT_NAME>` | remote_repo_exists |
| A08 | Подключить `origin` и выполнить push `main` | remote_synced |
| A09 | Проверить `git status`, `remote -v`, `log`, GitHub repo | bootstrap_verified |
| A10 | Зарегистрировать проект в FATHER Project Registry | father_registered |
| A11 | Привязать Agent Kit / K0 / K1 / K2 при наличии агента | knowledge_contract |
| A12 | Открыть C00 Intake и начать боевой конвейер | C00_OPEN |

## Immutable rule

`LOCAL PROJECT + GIT + PRIVATE GITHUB + BASELINE DOCS + C00 = STARTED`.

Проект не считается начатым только потому, что создана папка или репозиторий.

## Standard verification

```text
LOCAL ROOT
  ↓
GIT REPOSITORY
  ↓
BASELINE COMMIT
  ↓
PRIVATE GITHUB
  ↓
REMOTE PUSH
  ↓
FATHER REGISTRATION
  ↓
C00 INTAKE
```

## Universal stage contract

Любой последующий этап C00–C99 использует один контракт:

```text
INPUT
DEPENDENCIES
PROCESS
ARTIFACTS
VALIDATION
EVIDENCE
GATE
FAIL ACTION
OUTPUT
NEXT
```

Главное правило: **NO EVIDENCE → NO PROMOTION**.