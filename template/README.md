# Service

Python async backend service built with FastAPI, following hexagonal architecture.

## Stack

- Python 3.12+
- FastAPI — async REST API
- SQLAlchemy 2.x — ORM with `AsyncSession`
- Pydantic v2 — HTTP schemas in `interfaces`
- pytest — test framework
- Ruff — linter and formatter
- mypy — static type checker
- import-linter — hexagonal layer contracts

## Project layout

```
src/app/
  domain/           entities, exceptions, async ports — no frameworks
  application/      use cases that call ports
  infrastructure/   SQLAlchemy adapters that implement ports
  interfaces/api/   FastAPI routers + Pydantic schemas
  main.py           composition root
tests/
  unit/             use cases + fake ports
  fakes/            in-process adapters
  integration/      HTTP via build_app + SQLAlchemy repository
```

`GET /health` is a thin probe in `interfaces` (no domain).
`GET /notes/{note_id}` is the hexagonal example: async `NoteRepository` → use case → Pydantic response.

## Getting started

```bash
uv sync --extra dev
# or
python3.12 -m venv .venv && .venv/bin/pip install -e ".[dev]"
```

## Quality gate

```bash
bash scripts/run_quality_gate.sh
```

GitHub Actions runs the same script on every push to `main`/`master` and on pull requests (`.github/workflows/quality-gate.yml`).

## Run

```bash
uv run uvicorn app.main:app --reload
# or
.venv/bin/uvicorn app.main:app --reload
```
