"""Tests for the bank, accounts and ATM."""

from decimal import Decimal as D

import pytest
from banking_system.accounts import (
    BankError,
    InsufficientFundsError,
    LoanError,
    SavingsAccount,
    TxKind,
)
from banking_system.atm import ATM, AuthError
from banking_system.bank import Bank
from banking_system.cli import run


@pytest.fixture
def bank() -> Bank:
    # A fixture is reusable setup: any test that asks for `bank` gets a fresh one.
    b = Bank("Test")
    b.open_account("savings", "Ada", "a@x.io", "1111")
    b.open_account("current", "Bob", "b@x.io", "2222")
    return b


def test_deposit_withdraw_and_overdraft(bank: Bank) -> None:
    ada, bob = bank.get(1001), bank.get(1002)
    ada.deposit(D("100"))
    with pytest.raises(InsufficientFundsError):
        ada.withdraw(D("100.01"))
    bob.withdraw(D("300"))  # current account may overdraw up to 500
    assert bob.balance == D("-300.00")
    with pytest.raises(BankError):
        ada.deposit(D("-5"))


def test_transfer_and_totals(bank: Bank) -> None:
    bank.get(1001).deposit(D("50"))
    bank.transfer(1001, 1002, D("20"))
    assert bank.get(1002).history[-1].kind is TxKind.TRANSFER_IN
    assert bank.total_balance() == D("50")
    with pytest.raises(BankError):
        bank.transfer(1001, 9999, D("1"))


def test_loans(bank: Bank) -> None:
    bank.grant_loan(1001, D("10"))
    bank.grant_loan(1001, D("10"))
    with pytest.raises(LoanError):
        bank.grant_loan(1001, D("10"))
    bank.loans_enabled = False
    with pytest.raises(LoanError):
        bank.grant_loan(1002, D("10"))
    assert bank.total_loans() == D("20")


def test_interest(bank: Bank) -> None:
    acc = bank.get(1001)
    assert isinstance(acc, SavingsAccount)
    acc.deposit(D("100"))
    assert acc.add_interest() == D("3.00")


def test_atm_lockout(bank: Bank) -> None:
    bank.get(1001).deposit(D("100"))
    atm = ATM(bank)
    for _ in range(3):
        with pytest.raises(AuthError):
            atm.insert_card(1001, "0000")
    with pytest.raises(AuthError, match="locked"):
        atm.insert_card(1001, "1111")
    atm.insert_card(1002, "2222")
    with pytest.raises(BankError):
        atm.withdraw(D("15"))


def test_cli_flow() -> None:
    script = iter(
        [
            "1",
            "1",
            "savings",
            "Ada",
            "a@x",
            "1234",
            "3",
            "6",
            "2",
            "1001",
            "1",
            "50",
            "8",
            "3",
            "1001",
            "1234",
            "2",
            "20",
            "3",
            "9",
            "4",
        ]
    )
    out: list[str] = []
    run(Bank("T"), lambda _: next(script), out.append)
    assert "Opened Savings account #1001" in out
    assert out[-2] == "Balance: 30.00"
