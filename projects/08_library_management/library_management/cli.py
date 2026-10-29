"""Interactive library desk: `library`."""

from collections.abc import Callable
from datetime import date

from library_management.library import Library, LibraryError, demo_library


def run(
    lib: Library,
    ask: Callable[[str], str] = input,
    say: Callable[[str], None] = print,
    today: Callable[[], date] = date.today,
) -> None:
    menu = "\n1) Search 2) Borrow 3) Return 4) My loans 5) Overdue report 6) Exit: "
    while (c := ask(menu)) != "6":
        try:
            if c == "1":
                for b in lib.search(ask("Title/author: ")):
                    say(f"{b.isbn}  {b.title} by {b.author} ({lib.available(b.isbn)} available)")
            elif c == "2":
                loan = lib.borrow(int(ask("Member id: ")), ask("ISBN: "), today())
                say(f"Borrowed '{loan.book.title}', due {loan.due}")
            elif c == "3":
                fine = lib.return_book(int(ask("Member id: ")), ask("ISBN: "), today())
                say(f"Returned. Fine: {fine}")
            elif c == "4":
                member = lib.members[int(ask("Member id: "))]
                for loan in lib.active_loans(member):
                    say(f"{loan.book.title} due {loan.due}")
            elif c == "5":
                say(f"{len(lib.overdue(today()))} overdue loan(s)")
        except (LibraryError, ValueError, KeyError) as err:
            say(f"Error: {err}")


def main() -> int:
    try:
        run(demo_library())
    except (EOFError, KeyboardInterrupt):
        # Ctrl-D / Ctrl-C: leave cleanly instead of showing a traceback.
        print("\nGoodbye!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
