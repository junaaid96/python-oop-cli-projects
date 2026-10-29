# 23 · Decorators & context managers

## Decorators
A decorator takes a function and returns a new one.
```python
def retry(times: int = 3):  # decorator factory (takes arguments)
    def decorator(fn):
        @functools.wraps(fn)  # keep __name__, __doc__
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return fn(*args, **kwargs)
                except ConnectionError:
                    if attempt == times:
                        raise

        return wrapper

    return decorator


@retry(times=5)
def call_api() -> dict: ...
```
Built-ins to know: `@property`, `@classmethod`, `@staticmethod`, `@functools.cache`/`lru_cache`, `@dataclass`, `@contextmanager`. Django/DRF: `@login_required`, `@action`, `@transaction.atomic`. Typed version: see [20](20_advanced_typing.md).

## Context managers
Guarantee cleanup with `with`, even on exceptions.
```python
class Timer:
    def __enter__(self) -> "Timer":
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.elapsed = time.perf_counter() - self.start


@contextlib.contextmanager
def chdir_temp():
    old = os.getcwd()
    new = tempfile.mkdtemp()
    os.chdir(new)
    try:
        yield new
    finally:
        os.chdir(old)
```
`contextlib.suppress`, `ExitStack`, `closing`, `async with` (`__aenter__`/`__aexit__`).

## Exercises
1. Write `@timed` that logs runtime, and test it with `caplog`.
2. Write a context manager that temporarily sets an environment variable.
