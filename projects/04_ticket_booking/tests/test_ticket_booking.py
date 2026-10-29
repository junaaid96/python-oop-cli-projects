"""Tests for the ticket booking system."""

import pytest
from ticket_booking.cli import parse_seats, run
from ticket_booking.models import (
    InvalidSeatError,
    SeatTakenError,
    ShowNotFoundError,
    demo_cinema,
)


def test_booking_is_atomic() -> None:
    show = demo_cinema().find_show(111)
    show.book([(1, 1)])
    with pytest.raises(SeatTakenError):
        show.book([(1, 2), (1, 1)])
    # (1, 2) must NOT be booked because the whole request failed.
    assert show.booked == {(1, 1)}
    with pytest.raises(InvalidSeatError):
        show.book([(99, 1)])


def test_shows_have_separate_seats() -> None:
    cinema = demo_cinema()
    cinema.find_show(111).book([(2, 2)])
    assert cinema.find_show(333).booked == set()
    with pytest.raises(ShowNotFoundError):
        cinema.find_show(1)


def test_menu_flow() -> None:
    answers = iter(["2", "111", "1,1 1,2", "3", "111", "2", "111", "1,1", "4"])
    out: list[str] = []
    run(demo_cinema(), lambda _: next(answers), out.append)
    assert "Booked!" in out
    assert any(line.startswith("Error: seat (1, 1)") for line in out)
    assert parse_seats("3,4") == [(3, 4)]
