# 20 · Advanced typing

Builds on [07](07_dataclasses_and_typing.md). This repo runs `mypy --strict`.

```python
# Generics with PEP 695 syntax (3.12+)
class Repository[T]:
    def __init__(self) -> None:
        self._items: dict[int, T] = {}

    def add(self, key: int, item: T) -> None: ...
    def get(self, key: int) -> T | None: ...


def first[T](items: Sequence[T]) -> T:
    return items[0]


type Json = dict[str, "Json"] | list["Json"] | str | int | float | bool | None  # type alias
```

| Tool | Use |
|---|---|
| `Protocol` | structural ("duck") typing; see [05](05_abstraction.md) |
| `TypedDict` | typed dict shapes (JSON payloads) |
| `Literal["asc", "desc"]` | a fixed set of values |
| `Final`, `@final` | constants, no overriding |
| `Self` | methods returning their own class (`def copy(self) -> Self`) |
| `@overload` | different return types per argument types |
| `ParamSpec`, `Concatenate` | typing decorators that keep signatures |
| `TypeGuard` / `TypeIs` | custom narrowing functions |
| `NewType("UserId", int)` | distinct IDs that are ints at runtime |
| `@override` (3.12) | catch typos in overridden method names |
| `assert_never(x)` | exhaustive `match` on enums/unions |

```python
def logged[**P, R](fn: Callable[P, R]) -> Callable[P, R]:
    @functools.wraps(fn)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(fn.__name__)
        return fn(*args, **kwargs)

    return wrapper
```
Types are not checked at runtime; use pydantic or validation code at boundaries. Frameworks: `django-stubs` + `djangorestframework-stubs` give the Django project here typed QuerySets (see `pyproject.toml`).
