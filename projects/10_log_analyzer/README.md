# 10 · Log Analyzer (Intermediate) · functional style

Summarizes access logs: request count, status codes, top paths and p95 latency.

**Concepts:** generators and laziness, higher-order functions, closures, `functools.reduce`/`partial`, function composition, `collections.Counter`, `statistics`.

```bash
uv run log-analyzer access.log
uv run log-analyzer access.log --errors --prefix /api
```

## Exercises
1. Add `--since/--until` time filters as new predicate builders.
2. Group requests per minute with `itertools.groupby` and print a sparkline.
3. Support a second log format by passing the parser function as a parameter.
4. Process a 1 GB file and confirm memory stays flat (generators!).
