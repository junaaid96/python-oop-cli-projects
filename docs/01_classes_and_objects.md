# 01 · Classes and Objects

A **class** is a blueprint; an **object** (instance) is one thing built from it, with its own data.

```python
class Account:
    bank_name = "PyBank"  # class attribute: shared by every instance

    def __init__(self, owner: str, balance: int = 0) -> None:
        self.owner = owner  # instance attributes: one copy per object
        self.balance = balance

    def deposit(self, amount: int) -> None:  # method: behaviour that uses the object's data
        self.balance += amount

    def __repr__(self) -> str:  # how the object prints while debugging
        return f"Account({self.owner!r}, {self.balance})"


a = Account("Ana")
a.deposit(50)  # Python calls Account.deposit(a, 50); that `a` becomes `self`
```

## Kinds of methods
| Kind | Decorator | Receives | Use for |
|---|---|---|---|
| instance | none | `self` | normal behaviour |
| class | `@classmethod` | `cls` | alternate constructors (`from_dict`) |
| static | `@staticmethod` | nothing | helpers that belong with the class |
| property | `@property` | `self` | computed values that read like attributes |

## Useful dunder methods
`__repr__`, `__str__`, `__eq__`, `__lt__` (sorting), `__len__`, `__iter__`, `__contains__`, `__enter__/__exit__` (with-blocks).

**See it in:** 01 Contact Book (`ContactBook.__len__`, `__iter__`), 03 Todo (`Task.from_dict`).

## Practice
1. Add `__eq__` to a class and explain why two equal objects are not the same object (`is` vs `==`).
2. Write a `Temperature` class with a `fahrenheit` property computed from `celsius`.
