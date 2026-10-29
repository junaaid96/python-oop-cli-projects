"""Vehicles, spots, levels, tickets and pluggable pricing (Strategy pattern)."""

from __future__ import annotations

import math
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal

# IntEnum members compare like numbers, so SMALL < MEDIUM < LARGE works.
from enum import IntEnum
from itertools import count
from typing import ClassVar


class Size(IntEnum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3


class ParkingError(Exception):
    pass


@dataclass(frozen=True)
class Vehicle:
    plate: str
    size: Size = Size.MEDIUM


# Subclasses only change a default: no new behaviour needed, keep them tiny.
@dataclass(frozen=True)
class Motorcycle(Vehicle):
    size: Size = Size.SMALL


@dataclass(frozen=True)
class Car(Vehicle):
    size: Size = Size.MEDIUM


@dataclass(frozen=True)
class Truck(Vehicle):
    size: Size = Size.LARGE


@dataclass
class Spot:
    level: int
    number: int
    size: Size
    vehicle: Vehicle | None = None

    def fits(self, v: Vehicle) -> bool:
        # A vehicle fits any free spot of its size or bigger.
        return self.vehicle is None and v.size <= self.size

    @property
    def label(self) -> str:
        return f"L{self.level}-{self.number:02d}"


@dataclass(frozen=True)
class Ticket:
    id: int
    plate: str
    spot_label: str
    entered: datetime


class PricingStrategy(ABC):
    @abstractmethod
    def price(self, vehicle: Vehicle, hours: int) -> Decimal: ...


class HourlyPricing(PricingStrategy):
    # ClassVar: one shared, read-only table for the whole class.
    RATES: ClassVar[dict[Size, Decimal]] = {
        Size.SMALL: Decimal("1"),
        Size.MEDIUM: Decimal("2"),
        Size.LARGE: Decimal("4"),
    }

    def price(self, vehicle: Vehicle, hours: int) -> Decimal:
        return self.RATES[vehicle.size] * hours


class FlatDailyPricing(PricingStrategy):
    def __init__(self, per_day: Decimal = Decimal("15")) -> None:
        self.per_day = per_day

    def price(self, vehicle: Vehicle, hours: int) -> Decimal:
        return self.per_day * math.ceil(hours / 24)


@dataclass
class ParkingLot:
    pricing: PricingStrategy = field(default_factory=HourlyPricing)
    spots: list[Spot] = field(default_factory=list)
    _tickets: dict[str, tuple[Ticket, Spot]] = field(default_factory=dict)
    _ids: count[int] = field(default_factory=lambda: count(1))

    def add_level(self, level: int, layout: dict[Size, int]) -> None:
        n = 1
        for size, how_many in layout.items():
            for _ in range(how_many):
                self.spots.append(Spot(level, n, size))
                n += 1

    def free(self, size: Size | None = None) -> int:
        return sum(1 for s in self.spots if s.vehicle is None and size in (None, s.size))

    def park(self, vehicle: Vehicle, at: datetime) -> Ticket:
        if vehicle.plate in self._tickets:
            raise ParkingError(f"{vehicle.plate} is already parked")
        # Choose the smallest fitting spot so big spots stay free for big vehicles.
        candidates = sorted(
            (s for s in self.spots if s.fits(vehicle)), key=lambda s: (s.size, s.level, s.number)
        )
        if not candidates:
            raise ParkingError(f"no spot for a {vehicle.size.name.lower()} vehicle")
        spot = candidates[0]
        spot.vehicle = vehicle
        ticket = Ticket(next(self._ids), vehicle.plate, spot.label, at)
        self._tickets[vehicle.plate] = (ticket, spot)
        return ticket

    def leave(self, plate: str, at: datetime) -> Decimal:
        if plate not in self._tickets:
            raise ParkingError(f"{plate} is not parked here")
        ticket, spot = self._tickets.pop(plate)
        assert spot.vehicle is not None  # tells mypy (and readers) what we know
        # Any started hour is charged; minimum one hour.
        hours = max(1, math.ceil((at - ticket.entered).total_seconds() / 3600))
        fee = self.pricing.price(spot.vehicle, hours)
        spot.vehicle = None
        return fee


VEHICLES: dict[str, type[Vehicle]] = {"motorcycle": Motorcycle, "car": Car, "truck": Truck}


def demo_lot(pricing: PricingStrategy | None = None) -> ParkingLot:
    lot = ParkingLot(pricing or HourlyPricing())
    lot.add_level(1, {Size.SMALL: 2, Size.MEDIUM: 4, Size.LARGE: 1})
    lot.add_level(2, {Size.MEDIUM: 4, Size.LARGE: 1})
    return lot
