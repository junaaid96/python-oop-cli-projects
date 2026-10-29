# 19 · Iterators & generators

An **iterable** has `__iter__`; an **iterator** also has `__next__` and raises `StopIteration` when done. `for` loops call both for you.

```python
class Countdown:
    def __init__(self, start: int) -> None:
        self.current = start

    def __iter__(self) -> "Countdown":
        return self

    def __next__(self) -> int:
        if self.current <= 0:
            raise StopIteration
        self.current -= 1
        return self.current + 1
```

A **generator** writes the same thing with `yield` — state is kept between calls:
```python
def countdown(start: int) -> Iterator[int]:
    while start > 0:
        yield start
        start -= 1


squares = (n * n for n in range(10**9))  # generator expression: O(1) memory
```

- Lazy pipelines: `lines → parse → filter → aggregate` without loading the file (see [10 Log Analyzer](../projects/10_log_analyzer)).
- `yield from sub()` delegates to another generator.
- `itertools`: `islice`, `chain`, `groupby` (sort first!), `batched` (3.12+), `pairwise`, `accumulate`, `count`, `cycle`.
- A generator can be consumed **once**. Need it twice? Make a list or recreate it.
- Generator-based context managers: `@contextlib.contextmanager` with one `yield`.

Interview: *list vs generator?* List = all items in memory, reusable, `len()`; generator = lazy, one pass, constant memory.

## Exercises
1. Write `chunked(iterable, n)` without `itertools.batched`, with tests.
2. Turn a log-reading function into a three-stage generator pipeline.
