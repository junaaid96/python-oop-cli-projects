"""Tests for the contact book. Run with `uv run pytest`."""

from pathlib import Path

# pytest gives us fixtures (like tmp_path) and helpers (like pytest.raises).
import pytest
from contact_book.cli import main
from contact_book.models import Contact, ContactBook


def test_add_save_and_reload(tmp_path: Path) -> None:
    # tmp_path is a fresh temporary folder for every test.
    file = tmp_path / "c.json"
    book = ContactBook(file)
    book.add(Contact("Ada", "123", "ada@example.com"))
    book.save()
    # A brand-new object reading the same file proves persistence works.
    assert ContactBook(file).all() == [Contact("Ada", "123", "ada@example.com")]


def test_validation_and_duplicates(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        Contact("", "123")
    with pytest.raises(ValueError):
        Contact("Bob", "abc")
    book = ContactBook(tmp_path / "c.json")
    book.add(Contact("Bob", "1"))
    with pytest.raises(KeyError):
        book.add(Contact("bob", "2"))


def test_search_and_remove(tmp_path: Path) -> None:
    book = ContactBook(tmp_path / "c.json")
    book.add(Contact("Alan", "1", "alan@x.io"))
    book.add(Contact("Grace", "2"))
    assert [c.name for c in book.search("x.io")] == ["Alan"]
    book.remove("ALAN")
    assert len(book) == 1


def test_cli(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    f = str(tmp_path / "c.json")
    assert main(["--file", f, "add", "Linus", "555"]) == 0
    assert main(["--file", f, "list"]) == 0
    assert "Linus" in capsys.readouterr().out
    assert main(["--file", f, "remove", "Nobody"]) == 1
