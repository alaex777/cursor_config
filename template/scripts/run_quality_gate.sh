#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

run_tool() {
  local tool="$1"
  shift
  if command -v uv >/dev/null 2>&1; then
    uv run "$tool" "$@"
  elif [[ -x ".venv/bin/${tool}" ]]; then
    ".venv/bin/${tool}" "$@"
  else
    echo "Cannot find ${tool}. Install with: uv sync --extra dev" >&2
    echo "or: python3.12 -m venv .venv && .venv/bin/pip install -e '.[dev]'" >&2
    exit 1
  fi
}

run_tool ruff check .
run_tool ruff format --check .
run_tool mypy src
run_tool lint-imports
run_tool pytest
