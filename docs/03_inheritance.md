# 03 · Inheritance

A subclass **is a** more specific version of its parent and reuses its code.

```python
class Account:
    def __init__(self, owner: str) -> None:
        self.owner = owner
        self.balance = 0

    def monthly_fee(self) -> int:
        return 5


class StudentAccount(Account):
    def monthly_fee(self) -> int:  # override: same method name, new behaviour
        return 0


class SavingsAccount(Account):
    def __init__(self, owner: str, rate: float) -> None:
        super().__init__(owner)  # always let the parent set up its part
        self.rate = rate
```

## Rules of thumb
- Use it only for a true **is-a** relationship that holds for *every* method (Liskov Substitution).
- Keep hierarchies shallow (1–2 levels). Deep trees get fragile.
- `isinstance(x, Account)` works for subclasses too. Python's MRO (`Cls.__mro__`) decides lookup order with multiple inheritance.
- Small **mixins** (e.g. `JsonMixin`) are fine; when in doubt use composition ([06](06_composition_vs_inheritance.md)).

**See it in:** 06 Banking (`SavingsAccount`, `CurrentAccount`), 09 Parking Lot (vehicle types), 08 Library (member types).
