# Cursor Config

Personal Cursor AI configuration for Python backend development. Contains rules, roles, and agent definitions that guide AI behaviour across all projects.

## Structure

```
.cursor/
├── rules/      # Always-applied coding standards (alwaysApply: true)
├── roles/      # System-prompt personas for different task types
└── agents/     # Reusable agent definitions combining a role with a workflow
```

## Rules

Rules are automatically applied to every chat and agent session.

| Rule | Purpose |
|------|---------|
| `fastapi.mdc` | APIRouter, Dependency Injection, Pydantic v2, async endpoints, OpenAPI docs |
| `sqlalchemy.mdc` | SQLAlchemy 2.x, AsyncSession, repository pattern, no N+1 queries |
| `postgresql.mdc` | Indexes, query efficiency, constraints, pagination strategy |
| `testing.mdc` | pytest + fixtures, happy path / validation errors / edge cases |
| `security.mdc` | Auth, secrets, input validation; checks for SQLi, SSRF, IDOR |
| `code-quality.mdc` | Python 3.12+, type hints, Ruff style, small focused functions |

## Roles

Roles are system-prompt personas. Switch to a role when you need the AI to adopt a specific point of view.

| Role | When to use |
|------|-------------|
| `backend-engineer.md` | Implementing features, writing tests, refactoring |
| `architect.md` | Designing APIs, databases, evaluating tradeoffs |
| `reviewer.md` | Code review — bugs, security, performance, missing tests |

## Agents

Agents combine a role with a structured workflow for common recurring tasks.

| Agent | Goal |
|-------|------|
| `feature-developer.md` | Deliver production-ready backend features end-to-end |
| `architecture-advisor.md` | Produce architecture decisions before implementation begins |
| `pr-reviewer.md` | Find bugs, security risks, and performance issues before merge |
| `bug-investigator.md` | Trace execution flow to root cause rather than treating symptoms |

## Tech Stack

These configurations assume a Python backend built with:

- **FastAPI** — async REST API
- **SQLAlchemy 2.x** — ORM with `AsyncSession`
- **PostgreSQL** — primary database
- **pytest** — test framework
- **Ruff** — linter / formatter

## Usage

Clone or copy the `.cursor/` directory into any Python project to apply the same standards automatically.

```bash
git clone https://github.com/<you>/cursor_config.git
cp -r cursor_config/.cursor /path/to/your/project/
```

To activate a role in Cursor, reference the file in your chat system prompt or attach it at the start of a session.
