"""Tests use an in-memory SQLite database - fast and isolated."""

from datetime import date
from decimal import Decimal as D
from pathlib import Path

import pytest
from expense_tracker.cli import main
from expense_tracker.store import ExpenseStore, bar


def test_add_list_report() -> None:
    with ExpenseStore(":memory:") as s:
        s.add(date(2026, 10, 1), "Food", D("12.50"))
        s.add(date(2026, 10, 2), "rent", D("500"))
        s.add(date(2026, 9, 30), "food", D("1"))
        assert [e.category for e in s.list("2026-10")] == ["food", "rent"]
        assert s.totals_by_category("2026-10") == {"rent": D("500"), "food": D("12.50")}
        with pytest.raises(ValueError):
            s.add(date(2026, 1, 1), "x", D("0"))


def test_delete_and_bar() -> None:
    with ExpenseStore(":memory:") as s:
        e = s.add(date(2026, 1, 1), "x", D("1"))
        assert e.id is not None and s.delete(e.id)
        assert not s.delete(e.id)
    assert bar(D("5"), D("10"), width=10) == "#####"


def test_cli(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    db = str(tmp_path / "e.db")
    assert main(["--db", db, "add", "9.99", "books", "--date", "2026-10-05"]) == 0
    assert main(["--db", db, "report"]) == 0
    assert "books" in capsys.readouterr().out
    assert main(["--db", db, "add", "abc", "x"]) == 1
    assert main(["--db", db, "delete", "42"]) == 1
