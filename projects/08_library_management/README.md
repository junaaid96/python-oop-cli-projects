# 08 · Library Management (Intermediate)

Borrow and return books with per-member limits, due dates, fines and a waitlist.

**Concepts:** dataclass inheritance, overriding, `typing.Protocol`, Observer pattern, dependency injection, test doubles (fakes), `timedelta`.

```bash
uv run library
```

Demo members: `1` (student: 3 books / 14 days) and `2` (faculty: 10 books / 60 days).

## Exercises
1. Add an `EmailNotifier` that writes messages to an outbox file (no inheritance needed).
2. Persist to SQLite with tables `books`, `members`, `loans`.
3. Add reservations that expire after 2 days.
4. Add a librarian report: most borrowed books this month.
