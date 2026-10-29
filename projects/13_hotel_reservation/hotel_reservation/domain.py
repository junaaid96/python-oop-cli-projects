"""Pure domain objects: no database, no printing."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal
from enum import StrEnum


class ReservationError(Exception):
    pass


class RoomType(StrEnum):
    SINGLE = "single"
    DOUBLE = "double"
    SUITE = "suite"


@dataclass(frozen=True)
class Room:
    number: int
    type: RoomType
    nightly_rate: Decimal


@dataclass(frozen=True)
class Stay:
    """A value object for a date range; check_out is exclusive (like hotel nights)."""

    check_in: date
    check_out: date

    def __post_init__(self) -> None:
        if self.check_out <= self.check_in:
            raise ReservationError("check-out must be after check-in")

    @property
    def nights(self) -> int:
        return (self.check_out - self.check_in).days

    def overlaps(self, other: Stay) -> bool:
        # Two ranges overlap when each starts before the other ends.
        return self.check_in < other.check_out and other.check_in < self.check_out


@dataclass(frozen=True)
class Reservation:
    id: int
    guest: str
    room: Room
    stay: Stay
    cancelled: bool = False

    @property
    def total(self) -> Decimal:
        return self.room.nightly_rate * self.stay.nights

    def refund(self, today: date) -> Decimal:
        """Cancellation policy: full refund 7+ days before, 50% within 7 days, none after."""
        days_before = (self.stay.check_in - today).days
        if days_before >= 7:
            return self.total
        if days_before >= 0:
            return (self.total / 2).quantize(Decimal("0.01"))
        return Decimal("0")


def nights_between(stay: Stay) -> list[date]:
    return [stay.check_in + timedelta(days=i) for i in range(stay.nights)]
