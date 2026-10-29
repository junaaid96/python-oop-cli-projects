# 18 · OOP vs Functional: When to Use Which

Short answer: **model *things with state and rules* as objects; model *data transformations* as functions.** Most good Python mixes both.

| Choose **OOP** when… | Choose **functional** when… |
|---|---|
| entities have identity and changing state (account, ride, booking) | you transform data from input to output (logs → report) |
| rules must protect that state (no overdrafts) | steps are independent and composable |
| several variants share an interface (account types, payment methods) | you want easy parallelism / no shared state |
| you need to swap implementations (storage, strategies) | a class would just be `__init__` + one method |
| a long-lived process holds context (game, POS session) | scripts, data pipelines, one-shot CLIs |

## The same task, both ways
```python
# OOP: a stateful object guards its invariants
class Cart:
    def __init__(self) -> None:
        self._items: dict[str, int] = {}

    def add(self, sku: str, qty: int) -> None:
        if qty <= 0:
            raise ValueError("qty must be positive")
        self._items[sku] = self._items.get(sku, 0) + qty


# Functional: a pure function returns a new value
def add(cart: dict[str, int], sku: str, qty: int) -> dict[str, int]:
    return {**cart, sku: cart.get(sku, 0) + qty}
```

## The pragmatic hybrid (used across this repo)
1. **Immutable dataclasses** for values (`Point`, `Link`).
2. **Pure functions** for calculations (fares, totals, parsing).
3. **A few stateful service objects** for orchestration and I/O.
4. **Functions as strategies.** No class needed if one function will do.

**Warning signs:** a class with only `__init__` and one method → make it a function. Five functions passing the same 4 arguments around → make it a class.

Compare: 05 File Organizer and 10 Log Analyzer (functional) with 06 Banking and 13 Hotel (OOP).
