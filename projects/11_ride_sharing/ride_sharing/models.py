"""Users, vehicles, rides and the ride life-cycle (a small state machine)."""

from __future__ import annotations

import math
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from decimal import Decimal
from enum import StrEnum


class RideError(Exception):
    pass


@dataclass(frozen=True)
class Point:
    """A location on a simple grid (kilometres). Keeps the project place-neutral."""

    x: float
    y: float

    def distance_to(self, other: Point) -> float:
        # math.dist computes the straight-line (Euclidean) distance.
        return math.dist((self.x, self.y), (other.x, other.y))


class User(ABC):
    def __init__(self, name: str, email: str, national_id: str) -> None:
        self.name = name
        self.email = email
        self._national_id = national_id  # protected: personal data
        self._ratings: list[int] = []

    def rate(self, stars: int) -> None:
        if not 1 <= stars <= 5:
            raise RideError("rating must be 1-5")
        self._ratings.append(stars)

    @property
    def rating(self) -> float:
        return round(sum(self._ratings) / len(self._ratings), 2) if self._ratings else 5.0

    @abstractmethod
    def profile(self) -> str: ...


class VehicleType(StrEnum):
    BIKE = "bike"
    CAR = "car"
    PREMIUM = "premium"


# Fare table: base fare + per-km rate per vehicle type.
FARES: dict[VehicleType, tuple[Decimal, Decimal]] = {
    VehicleType.BIKE: (Decimal("1.00"), Decimal("0.50")),
    VehicleType.CAR: (Decimal("2.00"), Decimal("1.00")),
    VehicleType.PREMIUM: (Decimal("5.00"), Decimal("2.00")),
}


def fare(kind: VehicleType, km: float, surge: Decimal = Decimal("1")) -> Decimal:
    base, per_km = FARES[kind]
    return ((base + per_km * Decimal(str(round(km, 2)))) * surge).quantize(Decimal("0.01"))


class Driver(User):
    def __init__(
        self, name: str, email: str, national_id: str, vehicle: VehicleType, location: Point
    ) -> None:
        super().__init__(name, email, national_id)
        self.vehicle = vehicle
        self.location = location
        self.available = True
        self.earnings = Decimal("0")

    def profile(self) -> str:
        return f"Driver {self.name} ({self.vehicle}, {self.rating}*)"


class Rider(User):
    def __init__(
        self,
        name: str,
        email: str,
        national_id: str,
        location: Point,
        wallet: Decimal = Decimal("0"),
    ) -> None:
        super().__init__(name, email, national_id)
        self.location = location
        self.wallet = wallet
        self.current_ride: Ride | None = None

    def profile(self) -> str:
        return f"Rider {self.name} ({self.rating}*)"


class RideStatus(StrEnum):
    REQUESTED = "requested"
    STARTED = "started"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


# Allowed transitions: from-status -> set of next statuses.
TRANSITIONS: dict[RideStatus, set[RideStatus]] = {
    RideStatus.REQUESTED: {RideStatus.STARTED, RideStatus.CANCELLED},
    RideStatus.STARTED: {RideStatus.COMPLETED},
    RideStatus.COMPLETED: set(),
    RideStatus.CANCELLED: set(),
}


@dataclass
class Ride:
    rider: Rider
    driver: Driver
    start: Point
    end: Point
    price: Decimal
    status: RideStatus = RideStatus.REQUESTED
    log: list[RideStatus] = field(default_factory=lambda: [RideStatus.REQUESTED])

    def _move(self, new: RideStatus) -> None:
        if new not in TRANSITIONS[self.status]:
            raise RideError(f"cannot go from {self.status} to {new}")
        self.status = new
        self.log.append(new)

    def start_ride(self) -> None:
        self._move(RideStatus.STARTED)

    def complete(self) -> None:
        if self.rider.wallet < self.price:
            raise RideError("rider cannot pay; top up the wallet")
        self._move(RideStatus.COMPLETED)
        self.rider.wallet -= self.price
        self.driver.earnings += self.price
        self.driver.location = self.end
        self.rider.location = self.end
        self._release()

    def cancel(self) -> None:
        self._move(RideStatus.CANCELLED)
        self._release()

    def _release(self) -> None:
        self.driver.available = True
        self.rider.current_ride = None
