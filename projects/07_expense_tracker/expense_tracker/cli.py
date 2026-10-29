"""`expense-tracker add|list|report|delete` stored in SQLite."""

import argparse
from collections.abc import Sequence
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path

from expense_tracker.store import ExpenseStore, bar

DEFAULT_DB = Path.home() / ".python-oop-cli" / "expenses.db"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="expense-tracker")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    sub = parser.add_subparsers(dest="command", required=True)
    add = sub.add_parser("add")
    add.add_argument("amount")
    add.add_argument("category")
    add.add_argument("--note", default="")
    add.add_argument("--date", type=date.fromisoformat, default=date.today())
    for name in ("list", "report"):
        sub.add_parser(name).add_argument("--month", help="YYYY-MM")
    sub.add_parser("delete").add_argument("id", type=int)
    args = parser.parse_args(argv)

    args.db.parent.mkdir(parents=True, exist_ok=True)
    # `with` guarantees the database connection is closed.
    with ExpenseStore(args.db) as store:
        try:
            match args.command:
                case "add":
                    e = store.add(args.date, args.category, Decimal(args.amount), args.note)
                    print(f"Saved #{e.id}: {e.amount} on {e.category}")
                case "list":
                    for e in store.list(args.month):
                        print(f"#{e.id:<4} {e.spent_on} {e.category:<12} {e.amount:>10} {e.note}")
                case "report":
                    totals = store.totals_by_category(args.month)
                    top = max(totals.values(), default=Decimal("0"))
                    for cat, amount in totals.items():
                        print(f"{cat:<12} {amount:>10} {bar(amount, top)}")
                    print(f"{'TOTAL':<12} {sum(totals.values(), Decimal('0')):>10}")
                case "delete":
                    if not store.delete(args.id):
                        print(f"Error: no expense #{args.id}")
                        return 1
                    print("Deleted.")
        except (ValueError, InvalidOperation) as err:
            print(f"Error: {err}")
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
