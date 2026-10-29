"""Products and stock levels, with CSV import/export."""

from __future__ import annotations

import csv
from collections.abc import Callable
from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path


class StockError(Exception):
    pass


@dataclass(frozen=True)
class Product:
    sku: str
    name: str
    price: Decimal


@dataclass
class Inventory:
    reorder_level: int = 5
    _products: dict[str, Product] = field(default_factory=dict)
    _stock: dict[str, int] = field(default_factory=dict)
    # Callbacks run when stock drops low: a minimal Observer pattern using functions.
    on_low_stock: list[Callable[[Product, int], None]] = field(default_factory=list)

    def add(self, product: Product, qty: int) -> None:
        self._products[product.sku] = product
        self._stock[product.sku] = self._stock.get(product.sku, 0) + qty

    def product(self, sku: str) -> Product:
        if sku not in self._products:
            raise StockError(f"unknown SKU {sku}")
        return self._products[sku]

    def stock(self, sku: str) -> int:
        return self._stock.get(sku, 0)

    def remove(self, sku: str, qty: int) -> None:
        if self.stock(sku) < qty:
            raise StockError(f"only {self.stock(sku)} x {sku} left")
        self._stock[sku] -= qty
        if self._stock[sku] <= self.reorder_level:
            for callback in self.on_low_stock:
                callback(self._products[sku], self._stock[sku])

    def items(self) -> list[tuple[Product, int]]:
        return [(p, self._stock[s]) for s, p in sorted(self._products.items())]

    def export_csv(self, path: Path) -> None:
        # newline="" is required by the csv module to avoid blank lines on Windows.
        with path.open("w", newline="", encoding="utf-8") as fh:
            writer = csv.writer(fh)
            writer.writerow(["sku", "name", "price", "qty"])
            for p, qty in self.items():
                writer.writerow([p.sku, p.name, p.price, qty])

    @classmethod
    def from_csv(cls, path: Path) -> Inventory:
        inv = cls()
        with path.open(newline="", encoding="utf-8") as fh:
            # DictReader maps each row to {"sku": ..., "name": ...} using the header.
            for row in csv.DictReader(fh):
                inv.add(Product(row["sku"], row["name"], Decimal(row["price"])), int(row["qty"]))
        return inv
