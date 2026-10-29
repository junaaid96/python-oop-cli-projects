# 13 · Hotel Reservation (Advanced)

Search, book and cancel rooms stored in SQLite.

**Concepts:** layered architecture (domain → repository → service → CLI), value objects (`Stay`), interval overlap, business policies, `sqlite3.Row`, foreign keys.

```bash
uv run hotel search 2026-12-20 2026-12-23 --type double
uv run hotel book 2026-12-20 2026-12-23 --type double --guest "Ada Lovelace"
uv run hotel list
uv run hotel cancel 1
uv run hotel occupancy 2026-12-21
```

## Why layers?
Each layer has one reason to change (SRP). Swapping SQLite for another database only touches `repository.py`; changing the refund policy only touches `domain.py`.

## Exercises
1. Add seasonal pricing (weekend/holiday rates) as a pricing strategy.
2. Add room upgrades when the requested type is full.
3. Add an invoice with taxes and extras (breakfast, parking).
4. Write an `Repository` protocol and an in-memory implementation for faster tests.
