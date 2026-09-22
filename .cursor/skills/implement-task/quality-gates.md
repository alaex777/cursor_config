# Quality Gates Reference

Run from the service repo root. Prefer the repo script; otherwise resolve the runner.

## How to invoke tools

1. If `scripts/run_quality_gate.sh` exists → run it.
2. Else if `uv` is on `PATH` → prefix every tool with `uv run`.
3. Else if `.venv/bin/<tool>` exists → call that binary.
4. Else fail and tell the user to install:

```bash
uv sync --extra dev
# or
python3.12 -m venv .venv && .venv/bin/pip install -e ".[dev]"
```

Never call bare `ruff` / `mypy` / `pytest` / `lint-imports` — they are not guaranteed to be on `PATH`.

## Commands

```bash
ruff check .
ruff format --check .
mypy src
lint-imports
pytest
```

## Pass criteria

All five commands must exit with code 0.

## Ruff configuration (in pyproject.toml)

```toml
[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "UP", "B", "C4", "SIM"]
```

## mypy configuration (in pyproject.toml)

```toml
[tool.mypy]
python_version = "3.12"
strict = true
ignore_missing_imports = false
```

## pytest configuration (in pyproject.toml)

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

## Common failures and fixes

| Failure | Likely cause | Fix |
|---|---|---|
| `ruff: E501` | Line too long | Break line or increase `line-length` |
| `ruff: I001` | Unsorted imports | Run `ruff check --fix .` |
| `mypy: error: Missing return statement` | Async function missing return type | Add `-> ReturnType` |
| `mypy: error: Incompatible types` | Wrong type passed | Fix type annotation or cast |
| `lint-imports: BROKEN CONTRACT` | Cross-layer import | Move the symbol to the correct layer |
| `pytest: FAILED` | Assertion error | Check test fixture and use case logic |
| `pytest: ImportError` | Wrong import path | Check `src/` layout and `pythonpath` in pyproject.toml |
| `command not found: ruff` | Tools not installed / wrong runner | Use `uv run` or `.venv/bin/` |
