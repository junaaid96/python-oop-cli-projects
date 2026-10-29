"""Tests for the parking lot."""

from datetime import datetime, timedelta
from decimal import Decimal as D

import pytest
from parking_lot.cli import run
from parking_lot.lot import Car, FlatDailyPricing, Motorcycle, ParkingError, Size, Truck, demo_lot

T0 = datetime(2026, 1, 1, 8, 0)


def test_smallest_fitting_spot() -> None:
    lot = demo_lot()
    assert lot.park(Motorcycle("M1"), T0).spot_label == "L1-01"
    lot.park(Truck("T1"), T0)
    lot.park(Truck("T2"), T0)
    with pytest.raises(ParkingError, match="large"):
        lot.park(Truck("T3"), T0)
    assert lot.free(Size.LARGE) == 0


def test_pricing_strategies() -> None:
    lot = demo_lot()
    lot.park(Car("C1"), T0)
    assert lot.leave("C1", T0 + timedelta(hours=2, minutes=1)) == D("6")
    daily = demo_lot(FlatDailyPricing(D("10")))
    daily.park(Car("C2"), T0)
    assert daily.leave("C2", T0 + timedelta(hours=30)) == D("20")
    with pytest.raises(ParkingError):
        daily.leave("C2", T0)


def test_cli() -> None:
    script = iter(["1", "car", "ab1", "1", "car", "AB1", "2", "ab1", "3", "4"])
    out: list[str] = []
    run(demo_lot(), lambda _: next(script), out.append, lambda: T0)
    assert out[0] == "Ticket #1: spot L1-03"
    assert out[1].startswith("Error")
    assert "Fee: 2" in out
