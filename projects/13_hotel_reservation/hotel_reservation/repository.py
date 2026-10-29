"""Data access layer: the only module that writes SQL."""

from __future__ import annotations

import sqlite3
from datetime import date
from decimal import Decimal
from pathlib import Path

from hotel_reservation.domain import Reservation, Room, RoomType, Stay

SCHEMA = """
CREATE TABLE IF NOT EXISTS rooms (
    number INTEGER PRIMARY KEY,
    type   TEXT NOT NULL,
    rate   TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS reservations (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    guest     TEXT NOT NULL,
    room      INTEGER NOT NULL REFERENCES rooms(number),
    check_in  TEXT NOT NULL,
    check_out TEXT NOT NULL,
    cancelled INTEGER NOT NULL DEFAULT 0
);
"""


class Repository:
    def __init__(self, path: Path | str) -> None:
        self.conn = sqlite3.connect(str(path))
        # Row factory lets us access columns by name: row["guest"].
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.conn.executescript(SCHEMA)

    def add_room(self, room: Room) -> None:
        # `with conn:` commits automatically (or rolls back on error).
        with self.conn:
            self.conn.execute(
                "INSERT OR REPLACE INTO rooms VALUES (?, ?, ?)",
                (room.number, room.type.value, str(room.nightly_rate)),
            )

    def rooms(self) -> list[Room]:
        rows = self.conn.execute("SELECT * FROM rooms ORDER BY number")
        return [Room(r["number"], RoomType(r["type"]), Decimal(r["rate"])) for r in rows]

    def room(self, number: int) -> Room | None:
        return next((r for r in self.rooms() if r.number == number), None)

    def insert(self, guest: str, room: Room, stay: Stay) -> Reservation:
        with self.conn:
            cur = self.conn.execute(
                "INSERT INTO reservations (guest, room, check_in, check_out) VALUES (?, ?, ?, ?)",
                (guest, room.number, stay.check_in.isoformat(), stay.check_out.isoformat()),
            )
        assert cur.lastrowid is not None
        return Reservation(cur.lastrowid, guest, room, stay)

    def reservations(self, *, active_only: bool = True) -> list[Reservation]:
        sql = "SELECT * FROM reservations" + (" WHERE cancelled = 0" if active_only else "")
        rooms = {r.number: r for r in self.rooms()}
        return [
            Reservation(
                r["id"],
                r["guest"],
                rooms[r["room"]],
                Stay(date.fromisoformat(r["check_in"]), date.fromisoformat(r["check_out"])),
                bool(r["cancelled"]),
            )
            for r in self.conn.execute(sql + " ORDER BY check_in, id")
        ]

    def mark_cancelled(self, reservation_id: int) -> None:
        with self.conn:
            self.conn.execute(
                "UPDATE reservations SET cancelled = 1 WHERE id = ?", (reservation_id,)
            )
