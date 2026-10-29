"""Two interchangeable storage backends that satisfy the same Protocol."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass, replace
from datetime import datetime
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True)
class Link:
    id: int
    url: str
    code: str
    created: datetime
    expires: datetime | None = None
    clicks: int = 0


class LinkStore(Protocol):
    """The contract every backend must fulfil (Dependency Inversion)."""

    def next_id(self) -> int: ...
    def save(self, link: Link) -> None: ...
    def by_code(self, code: str) -> Link | None: ...
    def all(self) -> list[Link]: ...


class MemoryStore:
    def __init__(self) -> None:
        self._links: dict[str, Link] = {}

    def next_id(self) -> int:
        return len(self._links) + 1

    def save(self, link: Link) -> None:
        self._links[link.code] = link

    def by_code(self, code: str) -> Link | None:
        return self._links.get(code)

    def all(self) -> list[Link]:
        return list(self._links.values())


class SqliteStore:
    def __init__(self, path: Path | str) -> None:
        self._db = sqlite3.connect(str(path))
        self._db.execute(
            "CREATE TABLE IF NOT EXISTS links (id INTEGER PRIMARY KEY, url TEXT NOT NULL,"
            " code TEXT UNIQUE NOT NULL, created TEXT NOT NULL, expires TEXT,"
            " clicks INTEGER NOT NULL)"
        )

    def next_id(self) -> int:
        (value,) = self._db.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM links").fetchone()
        return int(value)

    def save(self, link: Link) -> None:
        with self._db:
            self._db.execute(
                "INSERT OR REPLACE INTO links VALUES (?, ?, ?, ?, ?, ?)",
                (
                    link.id,
                    link.url,
                    link.code,
                    link.created.isoformat(),
                    link.expires.isoformat() if link.expires else None,
                    link.clicks,
                ),
            )

    @staticmethod
    def _row(row: tuple[int, str, str, str, str | None, int]) -> Link:
        return Link(
            row[0],
            row[1],
            row[2],
            datetime.fromisoformat(row[3]),
            datetime.fromisoformat(row[4]) if row[4] else None,
            row[5],
        )

    def by_code(self, code: str) -> Link | None:
        row = self._db.execute("SELECT * FROM links WHERE code = ?", (code,)).fetchone()
        return self._row(row) if row else None

    def all(self) -> list[Link]:
        return [self._row(r) for r in self._db.execute("SELECT * FROM links ORDER BY id")]


def with_click(link: Link) -> Link:
    # Frozen dataclasses are updated by creating a modified copy.
    return replace(link, clicks=link.clicks + 1)
