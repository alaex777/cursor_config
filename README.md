# Cursor Config

Personal Cursor AI configuration and project template for Python async backend development.

## What's in this repo

```
.cursor/
  rules/       Coding standards for Python services
  roles/       System-prompt personas
  agents/      Pipeline subagents (orchestrator workspace only)
  skills/      implement-task orchestration (orchestrator workspace only)
template/      Hexagonal service scaffold + GitHub Actions
scripts/       init-service.sh
pipeline.yaml.example
README.md
```

Keep **skills and agents in this repo** (the orchestrator workspace). Copy **rules/roles only** into each service — never the pipeline skill.

## Rules

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
| `repo-sync` | fast | Fast-forward all repos onto `main_branch` |
| `planner` | full | Per-service plan, shared contracts, implementation waves |
| `implementer` | fast | One service; **resume** on rework |
| `quality-gate` | fast | ruff / mypy / import-linter / pytest in the service directory |
| `quality-fixer` | fast | Fixes quality-gate failures |
| `plan-auditor` | full | Diff vs plan (readonly) |
| `bug-hunter` | full | Serious bugs in new code |
| `task-auditor` | full | Cross-repo + shared contracts (readonly) |
| `git-shipper` | fast | Feature branch, commit, push — after approval |
| `docs-analyst` | full | Obsidian updates, or skip if no vault |
| `docs-writer` | fast | Applies the doc plan |
| `pr-reviewer` | full | Standalone PR review |

## Quickstart: new service

```bash
./scripts/init-service.sh /path/to/your-new-service
cd /path/to/your-new-service
# Edit pyproject.toml → [project] name
uv sync --extra dev
bash scripts/run_quality_gate.sh
```

The script copies the scaffold, GitHub Actions, and `.cursor/rules` + `.cursor/roles`. It does **not** copy pipeline skills or agents.

GitHub Actions (`.github/workflows/quality-gate.yml`) runs the same gate on push to `main`/`master` and on pull requests.

## Quickstart: multi-repo pipeline

Open **this** repository (or a workspace that contains it) in Cursor. Put `pipeline.yaml` next to it:

```yaml
main_branch: main
auto_push: false
obsidian_vault: /absolute/path/to/your/vault   # optional

repos:
  - name: billing
    path: ../billing
  - name: auth
    path: ../auth
```

See `pipeline.yaml.example`. Paths are relative to the directory that contains `pipeline.yaml`.

```
/implement-task

Task: <describe what you want to build>
Task ID: ABC-123
```

What runs:

1. Sync every listed repo to `main_branch` (`git pull --ff-only`). Stops on dirty trees.
2. Plan: shared contracts + implementation waves + per-service plans (saved to `.pipeline/<TASK_ID>.md`).
3. Implement wave by wave (parallel inside a wave). Implementers are **resumed** on rework.
4. Quality gate in each **changed** service (ruff, mypy, import-linter, pytest).
5. Plan audit → bug hunt → cross-repo task audit against shared contracts.
6. Show a ship summary. Push only after you confirm, unless `auto_push: true`.
7. Obsidian docs if `obsidian_vault` exists; otherwise skip.

If a custom `subagent_type` is missing from Task, the orchestrator falls back to `generalPurpose` plus `.cursor/agents/<name>.md`.

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

## Tech stack

- **FastAPI** — async REST API
- **SQLAlchemy 2.x** — ORM with `AsyncSession`
- **PostgreSQL** — primary database (`asyncpg`); SQLite for local/tests
- **pytest** — test framework with `asyncio_mode = auto`
- **Ruff** — linter + formatter
- **mypy** — static type checker (strict mode)
- **import-linter** — hexagonal import contracts
