"""Command-line interface: `contact-book add|list|search|remove`."""

# argparse is the standard-library tool for building CLIs.
import argparse

# Sequence is the type for "any list-like of str" (we accept argv for testing).
from collections.abc import Sequence
from pathlib import Path

from contact_book.models import Contact, ContactBook

# Default storage location inside the user's home folder.
DEFAULT_FILE = Path.home() / ".python-oop-cli" / "contacts.json"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="contact-book", description="Manage contacts.")
    # --file lets tests (and users) choose another JSON file.
    parser.add_argument("--file", type=Path, default=DEFAULT_FILE)
    # Sub-commands: each gets its own arguments.
    sub = parser.add_subparsers(dest="command", required=True)
    add = sub.add_parser("add", help="add a contact")
    add.add_argument("name")
    add.add_argument("phone")
    add.add_argument("--email", default="")
    sub.add_parser("list", help="list all contacts")
    search = sub.add_parser("search", help="search by name or email")
    search.add_argument("text")
    remove = sub.add_parser("remove", help="remove a contact")
    remove.add_argument("name")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    # argv=None means "use sys.argv"; tests pass a list instead.
    args = build_parser().parse_args(argv)
    book = ContactBook(args.file)
    try:
        # `match` (structural pattern matching) picks the branch for the command.
        match args.command:
            case "add":
                book.add(Contact(args.name, args.phone, args.email))
                book.save()
                print(f"Added {args.name}.")
            case "list":
                for c in book.all():
                    print(f"{c.name:<20} {c.phone:<15} {c.email}")
                print(f"{len(book)} contact(s)")
            case "search":
                for c in book.search(args.text):
                    print(f"{c.name:<20} {c.phone:<15} {c.email}")
            case "remove":
                book.remove(args.name)
                book.save()
                print(f"Removed {args.name}.")
    # Turn expected errors into friendly messages and a non-zero exit code.
    except (KeyError, ValueError) as err:
        print(f"Error: {err}")
        return 1
    return 0


# Allows `python -m contact_book.cli` as well as the installed `contact-book` command.
if __name__ == "__main__":
    raise SystemExit(main())
