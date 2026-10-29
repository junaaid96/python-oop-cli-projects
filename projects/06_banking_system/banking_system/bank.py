"""The Bank aggregates accounts. No global/class-level lists: each Bank owns its data."""

from __future__ import annotations

from decimal import Decimal

# itertools.count gives a simple increasing number generator for account ids.
from itertools import count

from banking_system.accounts import (
    Account,
    BankError,
    CurrentAccount,
    LoanError,
    SavingsAccount,
    TxKind,
)

# A registry maps a type name to its class: a tiny Factory.
ACCOUNT_TYPES: dict[str, type[Account]] = {"savings": SavingsAccount, "current": CurrentAccount}


class Bank:
    def __init__(self, name: str) -> None:
        self.name = name
        self._accounts: dict[int, Account] = {}
        self._numbers = count(1001)
        self.loans_enabled = True

    def open_account(self, kind: str, name: str, email: str, pin: str) -> Account:
        cls = ACCOUNT_TYPES.get(kind.lower())
        if cls is None:
            raise BankError(f"unknown account type {kind!r}; choose {sorted(ACCOUNT_TYPES)}")
        if not (pin.isdigit() and len(pin) == 4):
            raise BankError("PIN must be 4 digits")
        account = cls(next(self._numbers), name, email, pin)
        self._accounts[account.number] = account
        return account

    def get(self, number: int) -> Account:
        try:
            return self._accounts[number]
        except KeyError:
            raise BankError(f"account {number} does not exist") from None

    def close_account(self, number: int) -> None:
        self.get(number)
        del self._accounts[number]

    def accounts(self) -> list[Account]:
        return list(self._accounts.values())

    def total_balance(self) -> Decimal:
        # sum() needs a Decimal start value to keep the result a Decimal.
        return sum((a.balance for a in self._accounts.values()), Decimal("0"))

    def total_loans(self) -> Decimal:
        return sum((a.loan_total for a in self._accounts.values()), Decimal("0"))

    def grant_loan(self, number: int, amount: Decimal) -> None:
        if not self.loans_enabled:
            raise LoanError("loans are currently disabled by the bank")
        self.get(number).take_loan(amount)

    def transfer(self, source: int, target: int, amount: Decimal) -> None:
        if source == target:
            raise BankError("cannot transfer to the same account")
        sender, receiver = self.get(source), self.get(target)
        # Withdraw first: if it fails, nothing has been deposited yet.
        sender.withdraw(amount, TxKind.TRANSFER_OUT)
        receiver.deposit(amount, TxKind.TRANSFER_IN)
