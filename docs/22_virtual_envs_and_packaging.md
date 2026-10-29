# 22 · Virtual environments & packaging

Builds on [13 · Packaging and tooling](13_packaging_and_tooling.md).

## Why virtual environments
Each project gets its own interpreter + packages, so versions don't clash. A venv is just a folder (`.venv/`) with a `python` and `site-packages`.

| Tool | Command |
|---|---|
| stdlib | `python -m venv .venv && source .venv/bin/activate && pip install -e .` |
| **uv** (used here) | `uv sync` (creates `.venv`, installs from `uv.lock`), `uv run cmd` |
| pipx / `uv tool` | install CLI apps globally, isolated |

## pyproject.toml anatomy
```toml
[project]                   # PEP 621 metadata
name = "python-oop-cli-projects"
requires-python = ">=3.13"
dependencies = []           # runtime deps
[project.scripts]           # console commands
banking = "banking_system.cli:main"
[dependency-groups]         # PEP 735: dev/test/docs groups, not published
dev = ["pytest", "ruff", "mypy"]
[build-system]              # how to build a wheel
requires = ["hatchling"]
build-backend = "hatchling.build"
```
- **Lock files** (`uv.lock`) pin exact versions for reproducible installs; `pyproject.toml` holds ranges.
- `uv add django`, `uv add --group dev pytest`, `uv lock --upgrade`, `uv python install 3.13`.
- Build and publish: `uv build` → `dist/*.whl` + `*.tar.gz`; `uv publish` (use TestPyPI first, trusted publishing in CI).
- src layout (`src/pkg/`) avoids importing the uninstalled source by accident.
- Version specifiers: `>=6.0,<6.2` (range), `~=3.16` (compatible), `==` (pins, apps only).

## Exercises
1. Create a new package with `uv init --package demo`, add a script, build a wheel and install it in a fresh venv.
2. Explain the difference between `dependencies` and `dependency-groups`.
