# 14 · URL Shortener (Advanced)

Create short codes for links, resolve them, expire them and count clicks.

**Concepts:** `typing.Protocol` + Dependency Inversion, two interchangeable backends, base62 encoding, `dataclasses.replace`, `urllib.parse`, parametrized pytest fixtures (one test suite, two backends).

```bash
uv run url-shortener shorten https://docs.python.org/3/ --alias pydocs
uv run url-shortener open pydocs
uv run url-shortener stats
```

## Exercises
1. Serve redirects with `http.server` (a tiny web front-end).
2. Add a `JsonStore` backend; reuse the same parametrized tests.
3. Add per-day click history and a `stats --code X` chart.
4. Generate random, non-guessable codes with `secrets` and handle collisions.
