"""Tests for inventory and point of sale."""

from decimal import Decimal as D
from pathlib import Path

import pytest
from inventory_pos.cli import run
from inventory_pos.inventory import Inventory, Product, StockError
from inventory_pos.pos import (
    BestOf,
    BuyXGetYFree,
    Cart,
    PercentOff,
    Register,
    SpendThreshold,
    demo_register,
)


def test_discount_rules() -> None:
    pen = Product("P", "Pen", D("1"))
    items = [(pen, 7)]
    assert BuyXGetYFree("P", 2, 1).amount(items, D("7")) == D("2")
    assert PercentOff(D("10")).amount(items, D("7")) == D("0.7")
    best = BestOf((PercentOff(D("10")), SpendThreshold(D("5"), D("3"))))
    assert best.amount(items, D("7")) == D("3")


def test_checkout_totals_and_stock() -> None:
    reg = demo_register()
    cart = Cart()
    cart.add("B2", 3)
    cart.add("C3", 2)
    r = reg.checkout(cart)
    # subtotal 93.60; pen deal 1.20 + best(9.36, 7.00) = 10.56; tax 5% of 83.04 = 4.15
    assert (r.subtotal, r.discount, r.tax, r.total) == (
        D("93.60"),
        D("10.56"),
        D("4.15"),
        D("87.19"),
    )
    assert reg.inventory.stock("C3") == 4
    assert cart.lines == {}


def test_out_of_stock_is_atomic() -> None:
    reg = demo_register()
    cart = Cart()
    cart.add("A1", 1)
    cart.add("C3", 99)
    with pytest.raises(StockError):
        reg.checkout(cart)
    assert reg.inventory.stock("A1") == 20


def test_csv_roundtrip_and_low_stock(tmp_path: Path) -> None:
    inv = Inventory(reorder_level=2)
    inv.add(Product("X", "Thing", D("2.50")), 3)
    alerts: list[str] = []
    inv.on_low_stock.append(lambda p, n: alerts.append(f"{p.sku}:{n}"))
    inv.remove("X", 1)
    assert alerts == ["X:2"]
    inv.export_csv(tmp_path / "inv.csv")
    assert Inventory.from_csv(tmp_path / "inv.csv").items() == inv.items()


def test_cli() -> None:
    script = iter(["2", "c3", "2", "5", "2", "zz", "6", "7"])
    out: list[str] = []
    run(Register(demo_register().inventory, []), lambda _: next(script), out.append)
    assert any("TOTAL" in line for line in out)
    assert any(line.startswith("Error: unknown SKU") for line in out)
