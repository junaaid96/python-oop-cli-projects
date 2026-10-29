"""Tests for the library."""

from datetime import date, timedelta
from decimal import Decimal as D

import pytest
from library_management.cli import run
from library_management.library import Library, LibraryError, Member, demo_library

DAY = date(2026, 1, 1)


class FakeNotifier:
    """A test double that records messages instead of printing them."""

    def __init__(self) -> None:
        self.sent: list[tuple[str, str]] = []

    def send(self, member: Member, message: str) -> None:
        self.sent.append((member.name, message))


@pytest.fixture
def lib() -> Library:
    lib = demo_library()
    lib.notifiers = [FakeNotifier()]
    return lib


def test_borrow_limits_and_waitlist(lib: Library) -> None:
    lib.borrow(1, "978-0201633610", DAY)
    with pytest.raises(LibraryError, match="waitlist"):
        lib.borrow(2, "978-0201633610", DAY)
    lib.return_book(1, "978-0201633610", DAY)
    fake = lib.notifiers[0]
    assert isinstance(fake, FakeNotifier)
    assert fake.sent == [("Dr. Fay", "'Design Patterns' is now available")]


def test_fines_differ_by_member_type(lib: Library) -> None:
    lib.borrow(1, "978-0134757599", DAY)
    lib.borrow(2, "978-0134757599", DAY)
    late = DAY + timedelta(days=70)
    assert lib.return_book(1, "978-0134757599", late) == D("28.00")  # 56 days * 0.50
    assert lib.return_book(2, "978-0134757599", late) == D("2.50")  # 10 days * 0.25


def test_overdue_blocks_new_loans(lib: Library) -> None:
    lib.borrow(1, "978-1492056355", DAY)
    later = DAY + timedelta(days=20)
    assert len(lib.overdue(later)) == 1
    with pytest.raises(LibraryError, match="overdue"):
        lib.borrow(1, "978-0134757599", later)


def test_cli(lib: Library) -> None:
    script = iter(["1", "python", "2", "1", "978-1492056355", "3", "1", "bad", "6"])
    out: list[str] = []
    run(lib, lambda _: next(script), out.append, lambda: DAY)
    assert any("Fluent Python" in line for line in out)
    assert out[-1].startswith("Error")
