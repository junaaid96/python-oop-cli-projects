"""Lazy, composable processing of web-server style log lines.

Line format:  2026-10-30T10:15:00 GET /home 200 123ms
"""

from __future__ import annotations

import re
from collections import Counter
from collections.abc import Callable, Iterable, Iterator
from datetime import datetime

# reduce folds a sequence into one value; partial pre-fills function arguments.
from functools import partial, reduce
from statistics import quantiles
from typing import NamedTuple

LINE = re.compile(r"^(\S+) (GET|POST|PUT|DELETE|PATCH) (\S+) (\d{3}) (\d+)ms$")


class Entry(NamedTuple):
    at: datetime
    method: str
    path: str
    status: int
    ms: int


def parse(lines: Iterable[str]) -> Iterator[Entry]:
    """A generator: it yields entries one at a time, so huge files use little memory."""
    for line in lines:
        if m := LINE.match(line.strip()):
            yield Entry(datetime.fromisoformat(m[1]), m[2], m[3], int(m[4]), int(m[5]))


# Higher-order functions: they RETURN functions (predicates) built from parameters.
def status_at_least(code: int) -> Callable[[Entry], bool]:
    return lambda e: e.status >= code


def path_startswith(prefix: str) -> Callable[[Entry], bool]:
    return lambda e: e.path.startswith(prefix)


def all_of(*preds: Callable[[Entry], bool]) -> Callable[[Entry], bool]:
    # Combine many predicates into one; all() short-circuits on the first False.
    return lambda e: all(p(e) for p in preds)


type Step = Callable[[Iterable[Entry]], Iterable[Entry]]


def compose(*steps: Step) -> Step:
    """compose(f, g)(x) == g(f(x)) - build a pipeline from left to right."""
    return lambda data: reduce(lambda acc, step: step(acc), steps, data)


def where(pred: Callable[[Entry], bool]) -> Step:
    # partial(filter, pred) is a function still waiting for its iterable.
    return partial(filter, pred)


def top_paths(entries: Iterable[Entry], n: int = 5) -> list[tuple[str, int]]:
    return Counter(e.path for e in entries).most_common(n)


def status_counts(entries: Iterable[Entry]) -> dict[int, int]:
    return dict(sorted(Counter(e.status for e in entries).items()))


def latency_p95(entries: Iterable[Entry]) -> float:
    times = [e.ms for e in entries]
    if len(times) < 2:
        return float(times[0]) if times else 0.0
    # quantiles(n=20) gives 19 cut points; the last is the 95th percentile.
    return quantiles(times, n=20)[-1]


def summary(entries: Iterable[Entry]) -> dict[str, object]:
    # Materialize once because generators can only be consumed once.
    data = list(entries)
    return {
        "requests": len(data),
        "statuses": status_counts(data),
        "top_paths": top_paths(data, 3),
        "p95_ms": round(latency_p95(data), 1),
    }
