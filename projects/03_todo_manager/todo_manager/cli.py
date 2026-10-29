"""`todo add|list|done|delete` backed by a JSON file."""

import argparse
from collections.abc import Sequence
from datetime import date
from pathlib import Path

from todo_manager.models import Priority, TaskRepository

DEFAULT_FILE = Path.home() / ".python-oop-cli" / "todo.json"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="todo", description="A small task manager.")
    parser.add_argument("--file", type=Path, default=DEFAULT_FILE)
    sub = parser.add_subparsers(dest="command", required=True)
    add = sub.add_parser("add")
    add.add_argument("title")
    # choices= restricts input to the enum values and shows them in --help.
    add.add_argument("--priority", choices=[p.value for p in Priority], default="medium")
    # type=date.fromisoformat converts the text for us (and errors on bad dates).
    add.add_argument("--due", type=date.fromisoformat)
    add.add_argument("--tag", action="append", default=[])
    ls = sub.add_parser("list")
    ls.add_argument("--all", action="store_true")
    ls.add_argument("--tag")
    for name in ("done", "delete"):
        sub.add_parser(name).add_argument("id", type=int)
    args = parser.parse_args(argv)

    repo = TaskRepository(args.file)
    try:
        match args.command:
            case "add":
                task = repo.add(args.title, Priority(args.priority), args.due, args.tag)
                print(f"Added #{task.id}: {task.title}")
            case "list":
                today = date.today()
                for t in repo.list(include_done=args.all, tag=args.tag):
                    mark = "x" if t.done else " "
                    late = " (OVERDUE)" if t.is_overdue(today) else ""
                    due = t.due.isoformat() if t.due else "-"
                    print(f"[{mark}] #{t.id:<3} {t.priority:<6} {due:<10} {t.title}{late}")
            case "done":
                print(f"Completed: {repo.complete(args.id).title}")
            case "delete":
                repo.delete(args.id)
                print(f"Deleted #{args.id}")
    except KeyError as err:
        print(f"Error: {err.args[0]}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
