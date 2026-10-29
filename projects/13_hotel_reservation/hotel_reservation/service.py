"""Business rules live here. The service talks to the repository, never to SQL."""

from __future__ import annotations

from datetime import date
from decimal import Decimal

from hotel_reservation.domain import Reservation, ReservationError, Room, RoomType, Stay
from hotel_reservation.repository import Repository


class HotelService:
    def __init__(self, repo: Repository) -> None:
        self.repo = repo

    def available(self, stay: Stay, room_type: RoomType | None = None) -> list[Room]:
        busy = {r.room.number for r in self.repo.reservations() if r.stay.overlaps(stay)}
        return [
            room
            for room in self.repo.rooms()
            if room.number not in busy and room_type in (None, room.type)
        ]

    def book(self, guest: str, stay: Stay, room_type: RoomType) -> Reservation:
        if not guest.strip():
            raise ReservationError("guest name required")
        free = self.available(stay, room_type)
        if not free:
            raise ReservationError(f"no {room_type} room free for those dates")
        # Cheapest free room of the requested type.
        return self.repo.insert(guest, min(free, key=lambda r: r.nightly_rate), stay)

    def cancel(self, reservation_id: int, today: date) -> Decimal:
        match = [r for r in self.repo.reservations() if r.id == reservation_id]
        if not match:
            raise ReservationError(f"no active reservation #{reservation_id}")
        self.repo.mark_cancelled(reservation_id)
        return match[0].refund(today)

    def occupancy(self, day: date) -> float:
        rooms = self.repo.rooms()
        one_night = Stay(day, date.fromordinal(day.toordinal() + 1))
        taken = sum(1 for r in self.repo.reservations() if r.stay.overlaps(one_night))
        return round(100 * taken / len(rooms), 1) if rooms else 0.0


def seed(repo: Repository) -> None:
    if repo.rooms():
        return
    rates = {
        RoomType.SINGLE: Decimal("60"),
        RoomType.DOUBLE: Decimal("90"),
        RoomType.SUITE: Decimal("200"),
    }
    for number, kind in [
        (101, RoomType.SINGLE),
        (102, RoomType.SINGLE),
        (201, RoomType.DOUBLE),
        (202, RoomType.DOUBLE),
        (301, RoomType.SUITE),
    ]:
        repo.add_room(Room(number, kind, rates[kind]))
