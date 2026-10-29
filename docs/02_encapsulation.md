# 02 · Encapsulation

Keep an object's data valid by letting only its own methods change it.

```python
from decimal import Decimal


class Account:
    def __init__(self) -> None:
        self._balance = Decimal("0")  # leading underscore = "internal, please don't touch"

    @property
    def balance(self) -> Decimal:  # read-only from outside
        return self._balance

    def withdraw(self, amount: Decimal) -> None:
        if amount <= 0 or amount > self._balance:
            raise ValueError("invalid amount")  # the rule lives in ONE place
        self._balance -= amount
```

- `_name` is a convention for internal data; `__name` triggers name mangling (rarely needed).
- Prefer **methods that express intent** (`withdraw`) over setters (`set_balance`).
- Return copies or tuples, not your internal lists, so callers can't mutate them behind your back.
- `@dataclass(frozen=True)` gives you immutable value objects.

**See it in:** 06 Banking (`Account.balance`), 09 Parking Lot, 12 Inventory.

## Practice
Make a `Stack` class whose internal list can't be changed except via `push`/`pop`.
