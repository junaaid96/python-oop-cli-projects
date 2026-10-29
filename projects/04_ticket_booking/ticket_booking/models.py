"""Cinema, halls, shows and seat maps."""

from __future__ import annotations

from dataclasses import dataclass, field


# Custom exceptions make errors explicit and easy to catch selectively.
class BookingError(Exception):
    """Base class for every booking problem."""


class SeatTakenError(BookingError):
    pass


class InvalidSeatError(BookingError):
    pass


class ShowNotFoundError(BookingError):
    pass


# A seat is a (row, col) pair; a type alias gives it a readable name.
type Seat = tuple[int, int]


@dataclass
class Show:
    id: int
    movie: str
    time: str
    rows: int
    cols: int
    # Each show has its OWN seat map (the original version shared one per hall).
    booked: set[Seat] = field(default_factory=set)

    def _check(self, seat: Seat) -> None:
        row, col = seat
        # Chained comparisons read like maths: 1 <= row <= rows.
        if not (1 <= row <= self.rows and 1 <= col <= self.cols):
            raise InvalidSeatError(f"seat {seat} is outside the hall")

    def book(self, seats: list[Seat]) -> None:
        # Validate everything first so a booking is all-or-nothing (atomic).
        for seat in seats:
            self._check(seat)
            if seat in self.booked:
                raise SeatTakenError(f"seat {seat} is already booked")
        if len(set(seats)) != len(seats):
            raise BookingError("the same seat was requested twice")
        self.booked.update(seats)

    def available(self) -> int:
        return self.rows * self.cols - len(self.booked)

    def seat_map(self) -> str:
        # "O" = free, "X" = booked; a header row shows column numbers.
        header = "    " + " ".join(f"{c:>2}" for c in range(1, self.cols + 1))
        lines = [header]
        for r in range(1, self.rows + 1):
            cells = " ".join(
                " X" if (r, c) in self.booked else " O" for c in range(1, self.cols + 1)
            )
            lines.append(f"{r:>2}  {cells}")
        return "\n".join(lines)


@dataclass
class Hall:
    number: int
    rows: int
    cols: int
    shows: dict[int, Show] = field(default_factory=dict)

    def add_show(self, show_id: int, movie: str, time: str) -> Show:
        show = Show(show_id, movie, time, self.rows, self.cols)
        self.shows[show_id] = show
        return show


class Cinema:
    """Composition: a Cinema *has* halls (the original used inheritance, Hall(Star_Cinema))."""

    def __init__(self, name: str) -> None:
        self.name = name
        self._halls: list[Hall] = []

    def add_hall(self, hall: Hall) -> None:
        self._halls.append(hall)

    def shows(self) -> list[tuple[Hall, Show]]:
        return [(h, s) for h in self._halls for s in h.shows.values()]

    def find_show(self, show_id: int) -> Show:
        for _, show in self.shows():
            if show.id == show_id:
                return show
        raise ShowNotFoundError(f"show {show_id} not found")


def demo_cinema() -> Cinema:
    cinema = Cinema("Star Cinema")
    hall = Hall(101, rows=5, cols=8)
    hall.add_show(111, "3 Idiots", "2026-11-01 15:00")
    hall.add_show(333, "Chhichhore", "2026-11-02 18:00")
    cinema.add_hall(hall)
    return cinema
