# 17 · Functional Programming in Python

Python is multi-paradigm. Its functional toolbox:

```python
from functools import reduce, partial, cache
from itertools import groupby, islice

squares = [n * n for n in range(10) if n % 2 == 0]  # comprehension instead of map/filter
total = sum(x.amount for x in expenses)  # generator: lazy, constant memory
by_cat = {k: list(g) for k, g in groupby(sorted(items, key=cat), key=cat)}
add_tax = partial(price_with_tax, rate=0.15)  # pre-fill arguments


@cache
def fib(n: int) -> int:  # memoisation for pure functions
    return n if n < 2 else fib(n - 1) + fib(n - 2)
```

## Core ideas
- **Pure functions:** same input → same output, no side effects. Trivial to test.
- **Immutability:** `tuple`, `frozenset`, `@dataclass(frozen=True)`, `dataclasses.replace`.
- **Higher-order functions:** functions that take or return functions (`sorted(key=...)`, decorators).
- **Pipelines of generators:** read → parse → filter → aggregate, each stage tiny.

**See it in:** 05 File Organizer and 10 Log Analyzer, which are written mostly functionally.
