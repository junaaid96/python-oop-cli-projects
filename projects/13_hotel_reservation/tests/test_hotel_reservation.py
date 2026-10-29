"""Tests across the layers."""

from datetime import date
from decimal import Decimal as D
from pathlib import Path

import pytest
from hotel_reservation.cli import main
from hotel_reservation.domain import ReservationError, RoomType, Stay
from hotel_reservation.repository import Repository
from hotel_reservation.service import HotelService, seed


@pytest.fixture
def hotel() -> HotelService:
    repo = Repository(":memory:")
    seed(repo)
    return HotelService(repo)


def test_stay_rules() -> None:
    a = Stay(date(2026, 5, 1), date(2026, 5, 4))
    assert a.nights == 3
    assert a.overlaps(Stay(date(2026, 5, 3), date(2026, 5, 5)))
    assert not a.overlaps(Stay(date(2026, 5, 4), date(2026, 5, 6)))  # back-to-back is fine
    with pytest.raises(ReservationError):
        Stay(date(2026, 5, 2), date(2026, 5, 2))


def test_booking_and_availability(hotel: HotelService) -> None:
    stay = Stay(date(2026, 5, 1), date(2026, 5, 3))
    r = hotel.book("Ada", stay, RoomType.SUITE)
    assert r.total == D("400")
    with pytest.raises(ReservationError, match="suite"):
        hotel.book("Bob", stay, RoomType.SUITE)
    assert len(hotel.available(stay)) == 4
    assert hotel.occupancy(date(2026, 5, 2)) == 20.0


def test_cancellation_policy(hotel: HotelService) -> None:
    r = hotel.book("Ada", Stay(date(2026, 5, 10), date(2026, 5, 12)), RoomType.DOUBLE)
    assert hotel.cancel(r.id, date(2026, 5, 7)) == D("90.00")
    with pytest.raises(ReservationError):
        hotel.cancel(r.id, date(2026, 5, 7))


def test_cli(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    db = ["--db", str(tmp_path / "h.db")]
    assert main([*db, "book", "2026-06-01", "2026-06-02", "--guest", "Ada", "--type", "suite"]) == 0
    assert main([*db, "book", "2026-06-01", "2026-06-02", "--guest", "Bo", "--type", "suite"]) == 1
    assert main([*db, "list"]) == 0
    assert "Ada" in capsys.readouterr().out
