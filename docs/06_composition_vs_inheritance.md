# 06 · Composition vs Inheritance

**Composition** = an object *has* other objects and delegates work to them.

```python
class Engine:
    def start(self) -> str:
        return "vroom"


class Car:
    def __init__(self, engine: Engine) -> None:
        self.engine = engine  # has-a; swappable, easy to fake in tests

    def start(self) -> str:
        return self.engine.start()
```

## Why "prefer composition"
- Behaviour can change at runtime (inject a different strategy).
- No fragile base classes; each part is small and testable.
- Avoids class explosions like `ElectricSportsCarWithSunroof`.

## When inheritance is still right
- A genuine is-a relationship with a shared contract (`SavingsAccount` is an `Account`).
- Framework hooks that expect subclassing (`Exception`, `unittest.TestCase`).

**Smell test:** if a subclass overrides a method to *disable* it, use composition.

**See it in:** 09 Parking Lot (lot *has* a pricing strategy), 12 POS (`BestOf` composes discounts), 13 Hotel (service *has* a repository).
