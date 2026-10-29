# 04 · Polymorphism

"Many shapes": the same call does the right thing for different types.

```python
from typing import Protocol


class Shape(Protocol):
    def area(self) -> float: ...


class Square:
    def __init__(self, side: float) -> None:
        self.side = side

    def area(self) -> float:
        return self.side**2


class Circle:
    def __init__(self, r: float) -> None:
        self.r = r

    def area(self) -> float:
        return 3.14159 * self.r**2


def total(shapes: list[Shape]) -> float:
    return sum(s.area() for s in shapes)  # no if/elif on type needed
```

- **Duck typing:** Python cares that the method exists, not what the class is.
- **Operator overloading:** `__add__`, `__lt__`, `__len__` make your objects work with `+`, `sorted`, `len`.
- **`functools.singledispatch`** gives function-style polymorphism on argument type.
- **`match` statements** are great for data shapes; polymorphism is better when new types keep appearing.

A long `if type == "car": ... elif type == "bike": ...` chain is a hint to use polymorphism.

**See it in:** 08 Library (member types), 09 Parking Lot (pricing strategies), 12 Inventory/POS (discounts), 15 Text Adventure (commands).
