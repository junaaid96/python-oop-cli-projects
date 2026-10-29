"""A SQLite-backed expense store."""

from __future__ import annotations

# sqlite3 ships with Python: a full SQL database in a single file.
import sqlite3
from collections.abc import Iterator

# contextmanager turns a generator into a `with`-able object.
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS expenses (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    spent_on TEXT    NOT NULL,           -- ISO date
    category TEXT    NOT NULL,
    amount   TEXT    NOT NULL,           -- Decimal stored as text to stay exact
    note     TEXT    NOT NULL DEFAULT ''
);
"""


@dataclass(frozen=True)
class Expense:
    id: int | None
    spent_on: date
    category: str
    amount: Decimal
    note: str = ""


class ExpenseStore:
    def __init__(self, path: Path | str) -> None:
        # ":memory:" creates a throwaway database, perfect for tests.
        self._conn = sqlite3.connect(str(path))
        self._conn.executescript(SCHEMA)

    # A context manager ensures commit on success and rollback on error.
    @contextmanager
    def _tx(self) -> Iterator[sqlite3.Cursor]:
        cur = self._conn.cursor()
        try:
            yield cur
            self._conn.commit()
        except Exception:
            self._conn.rollback()
            raise
        finally:
            cur.close()

    def add(self, spent_on: date, category: str, amount: Decimal, note: str = "") -> Expense:
        if amount <= 0:
            raise ValueError("amount must be positive")
        with self._tx() as cur:
            # ALWAYS use ? placeholders: never build SQL with f-strings (SQL injection!).
            cur.execute(
                "INSERT INTO expenses (spent_on, category, amount, note) VALUES (?, ?, ?, ?)",
                (spent_on.isoformat(), category.lower(), str(amount), note),
            )
            new_id = cur.lastrowid
        return Expense(new_id, spent_on, category.lower(), amount, note)

    def delete(self, expense_id: int) -> bool:
        with self._tx() as cur:
            cur.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
            # rowcount tells how many rows were affected.
            return cur.rowcount == 1

    def list(self, month: str | None = None) -> list[Expense]:
        sql = "SELECT id, spent_on, category, amount, note FROM expenses"
        params: tuple[str, ...] = ()
        if month:  # month like "2026-10"; LIKE '2026-10%' matches all its days
            sql += " WHERE spent_on LIKE ?"
            params = (f"{month}%",)
        rows = self._conn.execute(sql + " ORDER BY spent_on, id", params).fetchall()
        return [Expense(r[0], date.fromisoformat(r[1]), r[2], Decimal(r[3]), r[4]) for r in rows]

    def totals_by_category(self, month: str | None = None) -> dict[str, Decimal]:
        # Summing in Python keeps Decimal precision (SQLite would use floats).
        totals: dict[str, Decimal] = {}
        for e in self.list(month):
            totals[e.category] = totals.get(e.category, Decimal("0")) + e.amount
        return dict(sorted(totals.items(), key=lambda kv: kv[1], reverse=True))

    def close(self) -> None:
        self._conn.close()

    # __enter__/__exit__ make ExpenseStore itself usable in a `with` block.
    def __enter__(self) -> ExpenseStore:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()


def bar(value: Decimal, maximum: Decimal, width: int = 30) -> str:
    """A text bar chart cell, e.g. '#########'."""
    return "#" * int(width * value / maximum) if maximum else ""
