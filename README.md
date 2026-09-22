# Cursor Config

Personal Cursor AI configuration and project template for Python async backend development.

## What's in this repo

```
.cursor/
  rules/       Coding standards applied automatically to every session
  roles/       System-prompt personas for different task types
  agents/      Custom subagents for the implementation pipeline
  skills/      Orchestration skill: implement-task pipeline
template/      Hexagonal service scaffold — copy to start a new service
pipeline.yaml.example  Template for wiring multiple repos to the pipeline
README.md      This file
```

## Rules (always applied)

| Rule | Purpose |
|---|---|
| `fastapi.mdc` | APIRouter in interfaces, Pydantic schemas, no Depends for use cases |
| `sqlalchemy.mdc` | SQLAlchemy 2.x, AsyncSession, repository implements a port |
| `postgresql.mdc` | Indexes, query efficiency, constraints, pagination |
| `testing.mdc` | pytest + fixtures, unit on use cases, integration on adapters |
| `security.mdc` | Auth, secrets, SQLi, SSRF, IDOR |
| `code-quality.mdc` | Python 3.12+, type hints, Ruff + mypy strict |
| `hexagonal.mdc` | Layer boundaries, async ports, composition root |
| `naming.mdc` | Intent-describing names, explicit keyword parameters |

## Roles

| Role | When to use |
|---|---|
| `backend-engineer.md` | Implementing features, writing tests, refactoring |
| `architect.md` | Designing APIs, defining ports, evaluating tradeoffs |
| `reviewer.md` | Code review — bugs, security, performance, missing tests |

## Pipeline agents

| Agent | Model | Purpose |
|---|---|---|
| `repo-sync` | fast | Checkout + pull `main_branch` in all repos |
| `planner` | full | Codebase analysis + per-service implementation plan |
| `implementer` | fast | Implements one service plan (hexagonal layers + tests) |
| `quality-gate` | fast | Runs ruff / mypy / import-linter / pytest |
| `quality-fixer` | fast | Fixes quality-gate failures |
| `plan-auditor` | full | Checks diff against the per-service plan |
| `bug-hunter` | full | Finds and fixes serious bugs in new code |
| `task-auditor` | full | Final cross-repo check against the original task |
| `git-shipper` | fast | Feature branch, conventional commit, push (never from main) |
| `docs-analyst` | full | Determines if Obsidian vault needs updates |
| `docs-writer` | fast | Applies the doc update plan to the vault |
| `pr-reviewer` | full | Standalone PR review (not a pipeline step) |

## Quickstart: new service

```bash
# 1. Copy the scaffold
cp -R template/. /path/to/your-new-service
cp -R .cursor   /path/to/your-new-service/

# 2. Rename the service in pyproject.toml
cd /path/to/your-new-service
# Edit pyproject.toml → [project] name = "your-service-name"

# 3. Install dev dependencies
uv sync --extra dev
# or
python3.12 -m venv .venv && .venv/bin/pip install -e ".[dev]"

# 4. Run quality gate
bash scripts/run_quality_gate.sh
```

GitHub Actions (`.github/workflows/quality-gate.yml`) runs that same gate on push to `main`/`master` and on pull requests.

## Quickstart: multi-repo pipeline

### 1. Create `pipeline.yaml` in your workspace root

```yaml
main_branch: main
obsidian_vault: /absolute/path/to/your/vault

repos:
  - name: billing
    path: ../billing
  - name: auth
    path: ../auth
```

See `pipeline.yaml.example` for a ready-to-copy template.

### 2. Run the pipeline

In Cursor Agent chat, type:

```
/implement-task

Task: <describe what you want to build>
Task ID: ABC-123
```

The skill will:
1. Sync all repos to `main_branch`
2. Analyse the codebase and produce a per-service plan
3. Spawn one implementer per service (in parallel, budget model)
4. Loop quality gates (ruff, mypy, import-linter, pytest) until all pass
5. Audit each service against the plan; fix gaps
6. Hunt serious bugs; fix and re-gate
7. Final cross-repo audit against the original task
8. Create `feat/<TASK_ID>-<slug>` branch, commit (Conventional Commits), push
9. Analyse Obsidian vault and update docs if needed

If a custom `subagent_type` is missing from Task, the orchestrator falls back to `generalPurpose` plus the matching `.cursor/agents/<name>.md` prompt.

## Service architecture (hexagonal)

```
src/app/
  domain/           entities, exceptions, async ports — no frameworks
  application/      use cases that call ports
  infrastructure/   SQLAlchemy adapters that implement ports
  interfaces/api/   FastAPI routers + Pydantic HTTP schemas
  main.py           composition root — wires infra to interfaces
tests/
  unit/             use cases with fake adapters
  integration/      HTTP via build_app + SQLAlchemy repository
```

The `template/` scaffold includes:

- `GET /health` — thin probe in `interfaces` (no domain)
- `GET /notes/{note_id}` — async `NoteRepository` port, SQLAlchemy adapter, use case, Pydantic schema

It passes `ruff`, `mypy --strict`, `lint-imports`, and `pytest` out of the box.

## Tech stack

- **FastAPI** — async REST API
- **SQLAlchemy 2.x** — ORM with `AsyncSession`
- **PostgreSQL** — primary database (`asyncpg`); SQLite for local/tests
- **pytest** — test framework with `asyncio_mode = auto`
- **Ruff** — linter + formatter
- **mypy** — static type checker (strict mode)
- **import-linter** — hexagonal import contracts
