# 07 · Expense Tracker (Intermediate)

Record spending in a SQLite database and print monthly reports with text bar charts.

**Concepts:** `sqlite3`, parameterized queries, transactions, context managers (`@contextmanager`, `__enter__`/`__exit__`), `Decimal`.

```bash
uv run expense-tracker add 12.50 food --note lunch
uv run expense-tracker list --month 2026-10
uv run expense-tracker report --month 2026-10
```

## Exercises
1. Add monthly budgets per category and warn when exceeded.
2. Import a bank CSV export.
3. Add a `trend` command comparing the last 6 months.
4. Add a schema version table and a migration that adds a `payment_method` column.
