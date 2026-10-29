"""Domain model for a small library."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from decimal import Decimal

# Protocol = structural typing: anything with a matching `send` method fits.
from typing import Protocol


class LibraryError(Exception):
    pass


@dataclass(frozen=True)
class Book:
    isbn: str
    title: str
    author: str


@dataclass
class Member:
    id: int
    name: str
    # Class-level constants that subclasses override (data-driven polymorphism).
    max_loans: int = 3
    loan_days: int = 14

    def fine_per_day(self) -> Decimal:
        return Decimal("0.50")


@dataclass
class StudentMember(Member):
    max_loans: int = 3
    loan_days: int = 14


@dataclass
class FacultyMember(Member):
    max_loans: int = 10
    loan_days: int = 60

    def fine_per_day(self) -> Decimal:
        return Decimal("0.25")  # overriding a method


@dataclass
class Loan:
    book: Book
    member: Member
    borrowed: date
    returned: date | None = None

    @property
    def due(self) -> date:
        return self.borrowed + timedelta(days=self.member.loan_days)

    def fine(self, on: date) -> Decimal:
        end = self.returned or on
        late_days = max(0, (end - self.due).days)
        return late_days * self.member.fine_per_day()


class Notifier(Protocol):
    """Any object with this method can receive notifications (Observer pattern)."""

    def send(self, member: Member, message: str) -> None: ...


class PrintNotifier:
    # No inheritance from Notifier needed: matching the shape is enough.
    def send(self, member: Member, message: str) -> None:
        print(f"[to {member.name}] {message}")


@dataclass
class Library:
    # Dependency injection: the notifier is passed in, so tests can use a fake.
    notifiers: list[Notifier] = field(default_factory=list)
    copies: dict[str, int] = field(default_factory=dict)
    books: dict[str, Book] = field(default_factory=dict)
    members: dict[int, Member] = field(default_factory=dict)
    loans: list[Loan] = field(default_factory=list)
    waitlist: dict[str, list[Member]] = field(default_factory=dict)

    def add_book(self, book: Book, copies: int = 1) -> None:
        self.books[book.isbn] = book
        self.copies[book.isbn] = self.copies.get(book.isbn, 0) + copies

    def join(self, member: Member) -> None:
        self.members[member.id] = member

    def _notify(self, member: Member, message: str) -> None:
        for n in self.notifiers:
            n.send(member, message)

    def active_loans(self, member: Member | None = None) -> list[Loan]:
        return [ln for ln in self.loans if ln.returned is None and member in (None, ln.member)]

    def available(self, isbn: str) -> int:
        out = sum(1 for ln in self.active_loans() if ln.book.isbn == isbn)
        return self.copies.get(isbn, 0) - out

    def search(self, text: str) -> list[Book]:
        t = text.lower()
        return [b for b in self.books.values() if t in b.title.lower() or t in b.author.lower()]

    def borrow(self, member_id: int, isbn: str, today: date) -> Loan:
        member, book = self.members[member_id], self.books.get(isbn)
        if book is None:
            raise LibraryError(f"no book with ISBN {isbn}")
        if len(self.active_loans(member)) >= member.max_loans:
            raise LibraryError(f"{member.name} reached the limit of {member.max_loans} loans")
        if any(ln.fine(today) > 0 for ln in self.active_loans(member)):
            raise LibraryError("return overdue books first")
        if self.available(isbn) <= 0:
            # Join the waitlist instead of failing silently.
            self.waitlist.setdefault(isbn, []).append(member)
            raise LibraryError(f"'{book.title}' is out; {member.name} added to the waitlist")
        loan = Loan(book, member, today)
        self.loans.append(loan)
        return loan

    def return_book(self, member_id: int, isbn: str, today: date) -> Decimal:
        member = self.members[member_id]
        for loan in self.active_loans(member):
            if loan.book.isbn == isbn:
                loan.returned = today
                if queue := self.waitlist.get(isbn):
                    self._notify(queue.pop(0), f"'{loan.book.title}' is now available")
                return loan.fine(today)
        raise LibraryError(f"{member.name} has not borrowed {isbn}")

    def overdue(self, today: date) -> list[Loan]:
        late = [ln for ln in self.active_loans() if today > ln.due]
        for loan in late:
            self._notify(loan.member, f"'{loan.book.title}' was due {loan.due}")
        return late


def demo_library() -> Library:
    lib = Library(notifiers=[PrintNotifier()])
    lib.add_book(Book("978-0134757599", "Refactoring", "Martin Fowler"), copies=2)
    lib.add_book(Book("978-0201633610", "Design Patterns", "Gamma et al."))
    lib.add_book(Book("978-1492056355", "Fluent Python", "Luciano Ramalho"))
    lib.join(StudentMember(1, "Sam"))
    lib.join(FacultyMember(2, "Dr. Fay"))
    return lib
