"""The ride sharing company: registers users and matches riders with drivers."""

from __future__ import annotations

from decimal import Decimal

from ride_sharing.models import Driver, Point, Ride, RideError, Rider, VehicleType, fare


class RideSharing:
    MAX_PICKUP_KM = 10.0

    def __init__(self, company: str) -> None:
        self.company = company
        self.riders: list[Rider] = []
        self.drivers: list[Driver] = []
        self.rides: list[Ride] = []

    def add_rider(self, rider: Rider) -> None:
        self.riders.append(rider)

    def add_driver(self, driver: Driver) -> None:
        self.drivers.append(driver)

    def surge(self) -> Decimal:
        # Simple supply/demand rule: few free drivers -> higher prices.
        free = sum(d.available for d in self.drivers)
        return Decimal("1.5") if free <= 1 else Decimal("1")

    def quote(self, start: Point, end: Point, kind: VehicleType) -> Decimal:
        return fare(kind, start.distance_to(end), self.surge())

    def request_ride(self, rider: Rider, destination: Point, kind: VehicleType) -> Ride:
        if rider.current_ride is not None:
            raise RideError(f"{rider.name} already has an active ride")
        candidates = [
            d
            for d in self.drivers
            if d.available
            and d.vehicle == kind
            and d.location.distance_to(rider.location) <= self.MAX_PICKUP_KM
        ]
        if not candidates:
            raise RideError(f"no {kind} driver nearby")
        # Nearest driver wins; ties go to the better-rated driver.
        driver = min(candidates, key=lambda d: (d.location.distance_to(rider.location), -d.rating))
        ride = Ride(
            rider,
            driver,
            rider.location,
            destination,
            self.quote(rider.location, destination, kind),
        )
        driver.available = False
        rider.current_ride = ride
        self.rides.append(ride)
        return ride

    def __repr__(self) -> str:
        return f"{self.company} has {len(self.drivers)} drivers and {len(self.riders)} riders"


def demo_service() -> RideSharing:
    app = RideSharing("PracticeRide")
    app.add_driver(Driver("Abid", "abid@example.com", "D-1", VehicleType.CAR, Point(1, 1)))
    app.add_driver(Driver("Mina", "mina@example.com", "D-2", VehicleType.CAR, Point(5, 5)))
    app.add_driver(Driver("Tariq", "tariq@example.com", "D-3", VehicleType.BIKE, Point(0, 2)))
    app.add_rider(Rider("Rakib", "rakib@example.com", "R-1", Point(0, 0), Decimal("100")))
    return app
