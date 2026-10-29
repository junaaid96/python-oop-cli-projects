"""Task model plus a JSON-backed repository."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field

# date handles calendar dates; we store them as ISO text ("2026-01-31") in JSON.
from datetime import date

# Enum gives a fixed set of named values instead of "magic strings".
from enum import StrEnum
from pathlib import Path


class Priority(StrEnum):
    # StrEnum members are also strings, so they serialize to JSON directly.
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class Task:
    id: int
    title: str
    priority: Priority = Priority.MEDIUM
    due: date | None = None
    done: bool = False
    tags: list[str] = field(default_factory=list)

    def is_overdue(self, today: date) -> bool:
        # A task is overdue if it has a due date in the past and isn't done.
        return not self.done and self.due is not None and self.due < today

    def to_dict(self) -> dict[str, object]:
        data = asdict(self)
        # Convert the date to text because JSON has no date type.
        data["due"] = self.due.isoformat() if self.due else None
        return data

    # @classmethod receives the class (cls), a common way to write alternative constructors.
    @classmethod
    def from_dict(cls, data: dict[str, object]) -> Task:
        due = data.get("due")
        raw_tags = data.get("tags")
        return cls(
            id=int(str(data["id"])),
            title=str(data["title"]),
            priority=Priority(str(data.get("priority", "medium"))),
            due=date.fromisoformat(due) if isinstance(due, str) else None,
            done=bool(data.get("done", False)),
            # isinstance() narrows the type, so mypy knows raw_tags is a list here.
            tags=[str(t) for t in raw_tags] if isinstance(raw_tags, list) else [],
        )


class TaskRepository:
    """The repository pattern: the rest of the app never touches JSON directly."""

    def __init__(self, path: Path) -> None:
        self._path = path
        self._tasks: dict[int, Task] = {}
        if path.exists():
            for item in json.loads(path.read_text(encoding="utf-8")):
                task = Task.from_dict(item)
                self._tasks[task.id] = task

    def _next_id(self) -> int:
        # max() with default handles the empty case.
        return max(self._tasks, default=0) + 1

    def add(
        self,
        title: str,
        priority: Priority = Priority.MEDIUM,
        due: date | None = None,
        tags: list[str] | None = None,
    ) -> Task:
        task = Task(self._next_id(), title, priority, due, tags=tags or [])
        self._tasks[task.id] = task
        self._save()
        return task

    def get(self, task_id: int) -> Task:
        if task_id not in self._tasks:
            raise KeyError(f"task {task_id} not found")
        return self._tasks[task_id]

    def complete(self, task_id: int) -> Task:
        task = self.get(task_id)
        task.done = True
        self._save()
        return task

    def delete(self, task_id: int) -> None:
        self.get(task_id)  # raises if missing
        del self._tasks[task_id]
        self._save()

    def list(self, *, include_done: bool = False, tag: str | None = None) -> list[Task]:
        # Keyword-only arguments (after *) make call sites self-explaining.
        order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
        tasks = [
            t
            for t in self._tasks.values()
            if (include_done or not t.done) and (tag is None or tag in t.tags)
        ]
        # Sort by priority first, then due date (tasks without a date go last).
        return sorted(tasks, key=lambda t: (order[t.priority], t.due or date.max, t.id))

    def _save(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        payload = [t.to_dict() for t in self._tasks.values()]
        self._path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
