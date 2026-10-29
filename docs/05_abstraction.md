# 05 · Abstraction: ABC vs Protocol

Hide *how*; expose *what*. Python has two tools.

```python
from abc import ABC, abstractmethod
from typing import Protocol


class PaymentMethod(ABC):  # nominal: you must inherit
    @abstractmethod
    def pay(self, amount: int) -> str: ...
    def receipt(self, amount: int) -> str:  # ABCs may share real code
        return f"Paid {amount}: {self.pay(amount)}"


class Storage(Protocol):  # structural: any class with these methods fits
    def save(self, key: str, value: str) -> None: ...
    def load(self, key: str) -> str | None: ...
```

| | ABC | Protocol |
|---|---|---|
| Needs inheritance | yes | no |
| Checked when | instantiating (`TypeError`) | by mypy |
| Shared code | yes | no (only the shape) |
| Best for | a family of classes you own | plugging in third-party / test doubles |

**See it in:** 08 Library (`Notifier` Protocol), 09 Parking Lot (`PricingStrategy` ABC), 12 POS (`Discount` ABC), 14 URL Shortener (`LinkStore` Protocol with two backends).
