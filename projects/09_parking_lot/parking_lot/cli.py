"""`parking-lot` interactive attendant console."""

import argparse
from collections.abc import Callable, Sequence
from datetime import datetime

from parking_lot.lot import (
    VEHICLES,
    FlatDailyPricing,
    HourlyPricing,
    ParkingError,
    ParkingLot,
    Size,
    demo_lot,
)


def run(
    lot: ParkingLot,
    ask: Callable[[str], str] = input,
    say: Callable[[str], None] = print,
    now: Callable[[], datetime] = datetime.now,
) -> None:
    while (c := ask("\n1) Park 2) Leave 3) Status 4) Exit: ")) != "4":
        try:
            if c == "1":
                kind = ask(f"Type {sorted(VEHICLES)}: ").lower()
                if kind not in VEHICLES:
                    raise ParkingError(f"unknown vehicle type {kind!r}")
                t = lot.park(VEHICLES[kind](ask("Plate: ").upper()), now())
                say(f"Ticket #{t.id}: spot {t.spot_label}")
            elif c == "2":
                say(f"Fee: {lot.leave(ask('Plate: ').upper(), now())}")
            elif c == "3":
                for size in Size:
                    say(f"{size.name:<7} free: {lot.free(size)}")
        except ParkingError as err:
            say(f"Error: {err}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="parking-lot")
    parser.add_argument("--pricing", choices=["hourly", "daily"], default="hourly")
    args = parser.parse_args(argv)
    try:
        run(demo_lot(FlatDailyPricing() if args.pricing == "daily" else HourlyPricing()))
    except (EOFError, KeyboardInterrupt):
        # Ctrl-D / Ctrl-C: leave cleanly instead of showing a traceback.
        print("\nGoodbye!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
