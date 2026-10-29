"""Interactive rider app: `ride-sharing`."""

from collections.abc import Callable
from decimal import Decimal

from ride_sharing.models import Point, RideError, VehicleType
from ride_sharing.service import RideSharing, demo_service


def read_point(ask: Callable[[str], str], label: str) -> Point:
    x, y = (float(v) for v in ask(f"{label} as x,y: ").split(","))
    return Point(x, y)


def run(
    app: RideSharing, ask: Callable[[str], str] = input, say: Callable[[str], None] = print
) -> None:
    rider = app.riders[0]
    say(f"Welcome {rider.name}! Wallet: {rider.wallet}. {app!r}")
    menu = "\n1) Quote 2) Request 3) Start 4) Complete 5) Cancel 6) Rate driver 7) Top up 8) Exit: "
    while (c := ask(menu)) != "8":
        try:
            ride = rider.current_ride
            if c == "1":
                kind = VehicleType(ask("Vehicle (bike/car/premium): "))
                say(
                    "Estimated fare: "
                    f"{app.quote(rider.location, read_point(ask, 'Destination'), kind)}"
                )
            elif c == "2":
                kind = VehicleType(ask("Vehicle (bike/car/premium): "))
                r = app.request_ride(rider, read_point(ask, "Destination"), kind)
                say(f"{r.driver.profile()} is coming. Fare {r.price}")
            elif c in {"3", "4", "5"}:
                if ride is None:
                    raise RideError("no active ride")
                {"3": ride.start_ride, "4": ride.complete, "5": ride.cancel}[c]()
                say(f"Ride is now {ride.status}. Wallet: {rider.wallet}")
            elif c == "6":
                last = next((r for r in reversed(app.rides) if r.rider is rider), None)
                if last is None:
                    raise RideError("no rides yet")
                last.driver.rate(int(ask("Stars 1-5: ")))
                say(last.driver.profile())
            elif c == "7":
                rider.wallet += Decimal(ask("Amount: "))
                say(f"Wallet: {rider.wallet}")
        except (RideError, ValueError) as err:
            say(f"Error: {err}")


def main() -> int:
    run(demo_service())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
