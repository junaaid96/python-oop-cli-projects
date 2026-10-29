"""Cashier console: `inventory-pos`."""

from collections.abc import Callable

from inventory_pos.inventory import Product, StockError
from inventory_pos.pos import Cart, Register, demo_register


def run(
    reg: Register, ask: Callable[[str], str] = input, say: Callable[[str], None] = print
) -> None:
    cart = Cart()

    def warn(product: Product, left: int) -> None:
        # A nested function used as a callback; it "closes over" `say`.
        say(f"! Low stock: {product.name} ({left} left)")

    reg.inventory.on_low_stock.append(warn)
    for d in reg.discounts:
        say(f"Deal: {d.describe()}")
    menu = "\n1) Stock 2) Add to cart 3) Remove 4) View cart 5) Checkout 6) Sales total 7) Exit: "
    while (c := ask(menu)) != "7":
        try:
            if c == "1":
                for p, qty in reg.inventory.items():
                    say(f"{p.sku:<4} {p.name:<12} {p.price:>7} stock {qty}")
            elif c == "2":
                sku = ask("SKU: ").upper()
                reg.inventory.product(sku)  # validate
                cart.add(sku, int(ask("Qty: ")))
            elif c == "3":
                cart.remove(ask("SKU: ").upper())
            elif c == "4":
                say(reg.quote(cart).render())
            elif c == "5":
                say(reg.checkout(cart).render())
            elif c == "6":
                say(f"Sales today: {reg.daily_total()} ({len(reg.sales)} receipts)")
        except (StockError, ValueError) as err:
            say(f"Error: {err}")


def main() -> int:
    run(demo_register())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
