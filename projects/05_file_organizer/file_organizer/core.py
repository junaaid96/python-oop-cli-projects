"""Pure functions: they only compute, they never touch the disk.

Functional style = "functional core, imperative shell". Everything here is easy to
test because the same input always gives the same output.
"""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from pathlib import PurePath
from typing import NamedTuple

# A plain mapping of category -> extensions. Data, not code, drives behaviour.
CATEGORIES: Mapping[str, frozenset[str]] = {
    "images": frozenset({".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"}),
    "documents": frozenset({".pdf", ".docx", ".txt", ".md", ".xlsx", ".pptx"}),
    "audio": frozenset({".mp3", ".wav", ".flac"}),
    "video": frozenset({".mp4", ".mkv", ".mov"}),
    "archives": frozenset({".zip", ".tar", ".gz", ".7z"}),
    "code": frozenset({".py", ".js", ".ts", ".java", ".cpp", ".html", ".css"}),
}


# NamedTuple: an immutable record, a lightweight alternative to a dataclass.
class Move(NamedTuple):
    source: PurePath
    target: PurePath


def categorize(name: PurePath, categories: Mapping[str, frozenset[str]] = CATEGORIES) -> str:
    # next() returns the first matching category, or "other" when none matches.
    suffix = name.suffix.lower()
    return next((cat for cat, exts in categories.items() if suffix in exts), "other")


def plan_moves(files: Iterable[PurePath], root: PurePath) -> list[Move]:
    # A comprehension builds the whole plan without mutating anything.
    return [Move(f, root / categorize(f) / f.name) for f in files if not f.name.startswith(".")]


def resolve_conflicts(moves: Iterable[Move], existing: frozenset[PurePath]) -> list[Move]:
    """Rename targets that would collide: photo.jpg -> photo (1).jpg."""
    taken = set(existing)  # local copy: the caller's data is never modified
    result: list[Move] = []
    for move in moves:
        target, n = move.target, 1
        while target in taken:
            target = move.target.with_name(f"{move.target.stem} ({n}){move.target.suffix}")
            n += 1
        taken.add(target)
        result.append(move._replace(target=target))
    return result


def summarize(moves: Iterable[Move]) -> dict[str, int]:
    # Counting with a dict comprehension over a sorted set of categories.
    cats = [m.target.parent.name for m in moves]
    return {c: cats.count(c) for c in sorted(set(cats))}
