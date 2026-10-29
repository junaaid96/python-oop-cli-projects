"""Accounts. Money uses Decimal, never float (0.1 + 0.2 != 0.3 with floats)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime

# Decimal gives exact base-10 arithmetic, which is what money needs.
from decimal import Decimal
from enum import StrEnum


class BankError(Exception):
    """Base class for banking errors."""


class InsufficientFundsError(BankError):
    pass


class LoanError(BankError):
    pass


class TxKind(StrEnum):
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"
    LOAN = "loan"
    TRANSFER_IN = "transfer in"
    TRANSFER_OUT = "transfer out"
    INTEREST = "interest"


@dataclass(frozen=True)
class Transaction:
    kind: TxKind
    amount: Decimal
    balance_after: Decimal
    # default_factory runs at creation time, so each transaction gets its own timestamp.
    at: datetime = field(default_factory=datetime.now)


def _positive(amount: Decimal) -> Decimal:
    if amount <= 0:
        raise BankError("amount must be positive")
    # quantize rounds to cents.
    return amount.quantize(Decimal("0.01"))


class Account(ABC):
    MAX_LOANS = 2  # class attribute: shared by every account

    def __init__(self, number: int, name: str, email: str, pin: str) -> None:
        self.number = number
        self.name = name
        self.email = email
        # Name-mangled (double underscore) so it's hard to read from outside.
        self.__pin = pin
        # Single underscore: internal, change only through methods below.
        self._balance = Decimal("0.00")
        self.loan_total = Decimal("0.00")
        self.loan_count = 0
        self._history: list[Transaction] = []

    # Read-only property: callers can read balance but not assign it.
    @property
    def balance(self) -> Decimal:
        return self._balance

    @property
    def history(self) -> tuple[Transaction, ...]:
        # Return an immutable copy so callers can't rewrite history.
        return tuple(self._history)

    def check_pin(self, pin: str) -> bool:
        return pin == self.__pin

    # Each subclass decides how far below zero it may go (polymorphism).
    @abstractmethod
    def withdraw_limit(self) -> Decimal: ...

    @property
    @abstractmethod
    def kind(self) -> str: ...

    def _record(self, kind: TxKind, amount: Decimal) -> None:
        self._history.append(Transaction(kind, amount, self._balance))

    def deposit(self, amount: Decimal, kind: TxKind = TxKind.DEPOSIT) -> None:
        amount = _positive(amount)
        self._balance += amount
        self._record(kind, amount)

    def withdraw(self, amount: Decimal, kind: TxKind = TxKind.WITHDRAW) -> None:
        amount = _positive(amount)
        if amount > self._balance + self.withdraw_limit():
            raise InsufficientFundsError(f"cannot withdraw {amount}; balance is {self._balance}")
        self._balance -= amount
        self._record(kind, amount)

    def take_loan(self, amount: Decimal) -> None:
        if self.loan_count >= self.MAX_LOANS:
            raise LoanError(f"loan limit of {self.MAX_LOANS} reached")
        self.deposit(amount, TxKind.LOAN)
        self.loan_total += _positive(amount)
        self.loan_count += 1


class SavingsAccount(Account):
    INTEREST_RATE = Decimal("0.03")

    @property
    def kind(self) -> str:
        return "Savings"

    def withdraw_limit(self) -> Decimal:
        return Decimal("0")  # savings can't go negative

    def add_interest(self) -> Decimal:
        interest = (self._balance * self.INTEREST_RATE).quantize(Decimal("0.01"))
        if interest > 0:
            self.deposit(interest, TxKind.INTEREST)
        return interest


class CurrentAccount(Account):
    OVERDRAFT = Decimal("500")

    @property
    def kind(self) -> str:
        return "Current"

    def withdraw_limit(self) -> Decimal:
        return self.OVERDRAFT
