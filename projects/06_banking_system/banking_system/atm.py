"""An ATM session: authenticate with a PIN, lock the card after 3 failures."""

from __future__ import annotations

from decimal import Decimal

from banking_system.accounts import BankError
from banking_system.bank import Bank


class AuthError(BankError):
    pass


class ATM:
    MAX_ATTEMPTS = 3

    def __init__(self, bank: Bank, cash: Decimal = Decimal("10000")) -> None:
        self._bank = bank
        self.cash = cash
        self._failed: dict[int, int] = {}
        self._session: int | None = None

    def insert_card(self, number: int, pin: str) -> None:
        if self._failed.get(number, 0) >= self.MAX_ATTEMPTS:
            raise AuthError("card is locked")
        account = self._bank.get(number)
        if not account.check_pin(pin):
            self._failed[number] = self._failed.get(number, 0) + 1
            raise AuthError(f"wrong PIN ({self.MAX_ATTEMPTS - self._failed[number]} tries left)")
        self._failed.pop(number, None)
        self._session = number

    def _current(self) -> int:
        if self._session is None:
            raise AuthError("insert card first")
        return self._session

    def balance(self) -> Decimal:
        return self._bank.get(self._current()).balance

    def withdraw(self, amount: Decimal) -> None:
        # ATMs dispense notes, so only multiples of 10 are allowed.
        if amount % 10 != 0:
            raise BankError("amount must be a multiple of 10")
        if amount > self.cash:
            raise BankError("ATM is out of cash")
        self._bank.get(self._current()).withdraw(amount)
        self.cash -= amount

    def eject(self) -> None:
        self._session = None
