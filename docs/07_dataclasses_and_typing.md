# 07 · Dataclasses, Enums and Type Hints

```python
from dataclasses import dataclass, field
from enum import StrEnum


class Priority(StrEnum):
    LOW = "low"
    HIGH = "high"


@dataclass(frozen=True, slots=True)  # immutable + memory-efficient
class Point:
    x: int
    y: int


@dataclass(order=True)
class Task:
    priority: int
    title: str = field(compare=False)
    tags: list[str] = field(default_factory=list)  # never use a bare [] default

    def __post_init__(self) -> None:  # validation hook
        if not self.title:
            raise ValueError("title required")
```

## Type-hint cheatsheet (3.13)
`list[int]`, `dict[str, float]`, `X | None`, `Callable[[str], int]`, `Iterator[T]`, `Self`, `ClassVar`, `Final`, generics: `class Box[T]: ...`.

Run `uv run mypy` to check them. Hints are documentation that a tool verifies.

**See it in:** every project; `dataclasses.replace` in 14, `field(default_factory=...)` in 03 and 15.
