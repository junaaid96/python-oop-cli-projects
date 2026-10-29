# 13 · Packaging and Tooling

This repo is one installable package defined in `pyproject.toml`.

```toml
[project.scripts]
banking = "banking.cli:main"     # `uv run banking` calls banking/cli.py:main()
```

| Tool | Command | Purpose |
|---|---|---|
| uv | `uv sync` | create `.venv` and install everything |
| ruff | `uv run ruff check .` / `ruff format .` | lint + format |
| mypy | `uv run mypy` | static type checking (strict) |
| pytest | `uv run pytest` | tests |
| GitHub Actions (optional) | `.github/workflows/ci.yml` | can run all of the above on every push; this repo runs them locally |

## Add your own project
1. Create `projects/16_my_app/my_app/{__init__,cli}.py` and `tests/test_my_app.py`.
2. Add the package to `[tool.hatch.build.targets.wheel] packages` and a script entry.
3. `uv sync && uv run my-app`.
