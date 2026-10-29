"""Cart, discount rules (Strategy + Composite) and checkout."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from decimal import ROUND_HALF_UP, Decimal

from inventory_pos.inventory import Inventory, Product, StockError

CENT = Decimal("0.01")


@dataclass
class Cart:
    lines: dict[str, int] = field(default_factory=dict)

    def add(self, sku: str, qty: int = 1) -> None:
        if qty <= 0:
            raise StockError("quantity must be positive")
        self.lines[sku] = self.lines.get(sku, 0) + qty

    def remove(self, sku: str) -> None:
        self.lines.pop(sku, None)


class Discount(ABC):
    """Each rule computes how much to take off. New rules = new classes (Open/Closed)."""

    @abstractmethod
    def amount(self, items: list[tuple[Product, int]], subtotal: Decimal) -> Decimal: ...

    @abstractmethod
    def describe(self) -> str: ...


@dataclass(frozen=True)
class PercentOff(Discount):
    percent: Decimal

    def amount(self, items: list[tuple[Product, int]], subtotal: Decimal) -> Decimal:
        return subtotal * self.percent / 100

    def describe(self) -> str:
        return f"{self.percent}% off"


@dataclass(frozen=True)
class BuyXGetYFree(Discount):
    sku: str
    buy: int
    free: int

    def amount(self, items: list[tuple[Product, int]], subtotal: Decimal) -> Decimal:
        for product, qty in items:
            if product.sku == self.sku:
                # Integer division: how many full "buy+free" groups are in the cart.
                return product.price * (qty // (self.buy + self.free)) * self.free
        return Decimal("0")

    def describe(self) -> str:
        return f"buy {self.buy} get {self.free} free on {self.sku}"


@dataclass(frozen=True)
class SpendThreshold(Discount):
    minimum: Decimal
    off: Decimal

    def amount(self, items: list[tuple[Product, int]], subtotal: Decimal) -> Decimal:
        return self.off if subtotal >= self.minimum else Decimal("0")

    def describe(self) -> str:
        return f"{self.off} off orders over {self.minimum}"


@dataclass(frozen=True)
class BestOf(Discount):
    """Composite: holds several discounts and applies only the best one."""

    options: tuple[Discount, ...]

    def amount(self, items: list[tuple[Product, int]], subtotal: Decimal) -> Decimal:
        return max((d.amount(items, subtotal) for d in self.options), default=Decimal("0"))

    def describe(self) -> str:
        return "best of: " + ", ".join(d.describe() for d in self.options)


@dataclass(frozen=True)
class Receipt:
    lines: list[tuple[Product, int, Decimal]]
    subtotal: Decimal
    discount: Decimal
    tax: Decimal
    total: Decimal

    def render(self) -> str:
        out = [f"{p.name:<18}{q:>3} x {p.price:>7} = {t:>8}" for p, q, t in self.lines]
        out += [
            f"{'Subtotal':<32}{self.subtotal:>8}",
            f"{'Discount':<32}{-self.discount:>8}",
            f"{'Tax':<32}{self.tax:>8}",
            f"{'TOTAL':<32}{self.total:>8}",
        ]
        return "\n".join(out)


class Register:
    def __init__(
        self,
        inventory: Inventory,
        discounts: list[Discount] | None = None,
        tax_rate: Decimal = Decimal("0.05"),
    ) -> None:
        self.inventory = inventory
        self.discounts = discounts or []
        self.tax_rate = tax_rate
        self.sales: list[Receipt] = []

    def quote(self, cart: Cart) -> Receipt:
        items = [(self.inventory.product(sku), q) for sku, q in cart.lines.items()]
        for product, qty in items:
            if self.inventory.stock(product.sku) < qty:
                raise StockError(f"not enough {product.name}")
        lines = [(p, q, p.price * q) for p, q in items]
        subtotal = sum((t for *_, t in lines), Decimal("0"))
        discount = min(
            subtotal, sum((d.amount(items, subtotal) for d in self.discounts), Decimal("0"))
        )
        discount = discount.quantize(CENT, ROUND_HALF_UP)
        tax = ((subtotal - discount) * self.tax_rate).quantize(CENT, ROUND_HALF_UP)
        return Receipt(lines, subtotal, discount, tax, subtotal - discount + tax)

    def checkout(self, cart: Cart) -> Receipt:
        receipt = self.quote(cart)
        # Only touch stock after the whole quote succeeded.
        for p, q, _ in receipt.lines:
            self.inventory.remove(p.sku, q)
        self.sales.append(receipt)
        cart.lines.clear()
        return receipt

    def daily_total(self) -> Decimal:
        return sum((r.total for r in self.sales), Decimal("0"))


def demo_register() -> Register:
    inv = Inventory()
    inv.add(Product("A1", "Notebook", Decimal("3.50")), 20)
    inv.add(Product("B2", "Pen", Decimal("1.20")), 50)
    inv.add(Product("C3", "Backpack", Decimal("45.00")), 6)
    deals = BestOf((PercentOff(Decimal("10")), SpendThreshold(Decimal("50"), Decimal("7"))))
    return Register(inv, [BuyXGetYFree("B2", 2, 1), deals])
