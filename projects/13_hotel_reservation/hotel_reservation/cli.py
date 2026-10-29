"""`hotel search|book|cancel|list|occupancy`"""

import argparse
from collections.abc import Sequence
from datetime import date
from pathlib import Path

from hotel_reservation.domain import ReservationError, RoomType, Stay
from hotel_reservation.repository import Repository
from hotel_reservation.service import HotelService, seed

DEFAULT_DB = Path.home() / ".python-oop-cli" / "hotel.db"


def main(argv: Sequence[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="hotel")
    p.add_argument("--db", type=Path, default=DEFAULT_DB)
    sub = p.add_subparsers(dest="command", required=True)
    for name in ("search", "book"):
        s = sub.add_parser(name)
        s.add_argument("check_in", type=date.fromisoformat)
        s.add_argument("check_out", type=date.fromisoformat)
        s.add_argument("--type", choices=[t.value for t in RoomType])
        if name == "book":
            s.add_argument("--guest", required=True)
    sub.add_parser("cancel").add_argument("id", type=int)
    sub.add_parser("list")
    sub.add_parser("occupancy").add_argument("day", type=date.fromisoformat)
    args = p.parse_args(argv)

    args.db.parent.mkdir(parents=True, exist_ok=True)
    repo = Repository(args.db)
    seed(repo)
    hotel = HotelService(repo)
    try:
        match args.command:
            case "search":
                stay = Stay(args.check_in, args.check_out)
                kind = RoomType(args.type) if args.type else None
                for room in hotel.available(stay, kind):
                    print(
                        f"Room {room.number} {room.type:<7} {room.nightly_rate}/night "
                        f"= {room.nightly_rate * stay.nights}"
                    )
            case "book":
                r = hotel.book(
                    args.guest, Stay(args.check_in, args.check_out), RoomType(args.type or "single")
                )
                print(
                    f"Reservation #{r.id}: room {r.room.number}, "
                    f"{r.stay.nights} nights, total {r.total}"
                )
            case "cancel":
                print(f"Cancelled. Refund: {hotel.cancel(args.id, date.today())}")
            case "list":
                for r in repo.reservations():
                    print(
                        f"#{r.id} {r.guest:<15} room {r.room.number} "
                        f"{r.stay.check_in} -> {r.stay.check_out}"
                    )
            case "occupancy":
                print(f"Occupancy: {hotel.occupancy(args.day)}%")
    except ReservationError as err:
        print(f"Error: {err}")
        return 1
    finally:
        repo.conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
