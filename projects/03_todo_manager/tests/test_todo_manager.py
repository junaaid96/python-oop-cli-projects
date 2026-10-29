"""Tests for the todo manager."""

from datetime import date
from pathlib import Path

import pytest
from todo_manager.cli import main
from todo_manager.models import Priority, TaskRepository


def test_add_complete_persist(tmp_path: Path) -> None:
    file = tmp_path / "t.json"
    repo = TaskRepository(file)
    a = repo.add("write tests", Priority.HIGH, date(2026, 1, 1), ["dev"])
    repo.add("relax", Priority.LOW)
    repo.complete(a.id)
    reloaded = TaskRepository(file)
    assert [t.title for t in reloaded.list()] == ["relax"]
    assert reloaded.get(a.id).done
    assert [t.title for t in reloaded.list(include_done=True, tag="dev")] == ["write tests"]


def test_overdue_and_sorting(tmp_path: Path) -> None:
    repo = TaskRepository(tmp_path / "t.json")
    late = repo.add("late", Priority.LOW, date(2020, 1, 1))
    repo.add("urgent", Priority.HIGH)
    assert late.is_overdue(date(2026, 1, 1))
    assert repo.list()[0].title == "urgent"


def test_cli_errors(tmp_path: Path) -> None:
    f = str(tmp_path / "t.json")
    assert main(["--file", f, "add", "x", "--due", "2026-02-01", "--tag", "a"]) == 0
    assert main(["--file", f, "done", "99"]) == 1
    with pytest.raises(SystemExit):
        main(["--file", f, "add", "x", "--priority", "extreme"])
