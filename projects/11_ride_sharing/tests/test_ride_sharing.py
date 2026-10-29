"""Tests for the ride sharing service."""

from decimal import Decimal as D

import pytest
from ride_sharing.cli import run
from ride_sharing.models import Point, RideError, RideStatus, VehicleType, fare
from ride_sharing.service import demo_service


def test_fare() -> None:
    assert fare(VehicleType.CAR, 3.0) == D("5.00")
    assert fare(VehicleType.BIKE, 2.0, D("1.5")) == D("3.00")


def test_nearest_driver_and_lifecycle() -> None:
    app = demo_service()
    rider = app.riders[0]
    ride = app.request_ride(rider, Point(3, 4), VehicleType.CAR)
    assert ride.driver.name == "Abid"
    with pytest.raises(RideError):
        app.request_ride(rider, Point(1, 1), VehicleType.CAR)
    with pytest.raises(RideError):
        ride.complete()  # must start first
    ride.start_ride()
    ride.complete()
    assert ride.log == [RideStatus.REQUESTED, RideStatus.STARTED, RideStatus.COMPLETED]
    assert rider.wallet == D("100") - ride.price
    assert ride.driver.earnings == ride.price and ride.driver.available


def test_no_driver_and_ratings() -> None:
    app = demo_service()
    with pytest.raises(RideError, match="premium"):
        app.request_ride(app.riders[0], Point(1, 1), VehicleType.PREMIUM)
    d = app.drivers[0]
    d.rate(4)
    d.rate(5)
    assert d.rating == 4.5
    with pytest.raises(RideError):
        d.rate(6)


def test_cli() -> None:
    script = iter(["2", "bike", "3,4", "3", "4", "6", "5", "5", "8"])
    out: list[str] = []
    run(demo_service(), lambda _: next(script), out.append)
    assert out[1].startswith("Driver Tariq")
    assert "Ride is now completed" in out[3]
    assert out[-1] == "Error: no active ride"
