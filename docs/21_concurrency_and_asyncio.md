# 21 · Concurrency & asyncio

| Work type | Tool | Why |
|---|---|---|
| Waiting on network/disk (I/O-bound), many tasks | `asyncio` | thousands of tasks on one thread |
| I/O-bound with blocking libraries | `threading` / `ThreadPoolExecutor` | the GIL is released while waiting |
| CPU-bound (math, image work) | `multiprocessing` / `ProcessPoolExecutor` | separate processes, separate GILs |

Python 3.13 also ships an experimental **free-threaded** build (no GIL, `python3.13t`); 3.14 makes it officially supported. Most code still targets the normal build.

## asyncio
```python
import asyncio


async def fetch(name: str, delay: float) -> str:
    await asyncio.sleep(delay)  # yields control instead of blocking
    return name


async def main() -> None:
    async with asyncio.TaskGroup() as tg:  # 3.11+: structured concurrency
        a = tg.create_task(fetch("a", 1))
        b = tg.create_task(fetch("b", 1))
    print(a.result(), b.result())  # ~1 s total, not 2

    async with asyncio.timeout(2):  # 3.11+
        await fetch("slow", 1)


asyncio.run(main())
```
- `await` only inside `async def`. Never call blocking code (`time.sleep`, `requests`) in a coroutine; use `await asyncio.to_thread(fn)`.
- `asyncio.gather` (older), `Semaphore` to limit concurrency, `Queue` for producer/consumer.
- Errors in a `TaskGroup` cancel siblings and raise an `ExceptionGroup` (`except*`).

## Threads & processes
```python
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

with ThreadPoolExecutor(max_workers=8) as pool:
    results = list(pool.map(download, urls))
```
Shared mutable state needs a `threading.Lock`; better, pass messages (`queue.Queue`).

In Django: async views and `aget()`/`afilter()` ORM methods exist, but blocking work belongs in Celery ([django/11](django/11_caching_and_celery.md)).

## Exercises
1. Download 20 URLs with a `Semaphore(5)` and a `TaskGroup`.
2. Time a CPU-heavy function with threads vs processes and explain the result.
