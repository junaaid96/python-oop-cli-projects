"""Menu-driven CLI with Admin, Customer and ATM sections: `banking`."""

from collections.abc import Callable
from decimal import Decimal, InvalidOperation

from banking_system.accounts import BankError, SavingsAccount
from banking_system.atm import ATM
from banking_system.bank import Bank

Ask = Callable[[str], str]
Say = Callable[[str], None]


def admin_menu(bank: Bank, ask: Ask, say: Say) -> None:
    while (
        c := ask("\n[Admin] 1) Open 2) Close 3) List 4) Totals 5) Toggle loans 6) Back: ")
    ) != "6":
        # The walrus operator := assigns and tests in one expression.
        if c == "1":
            acc = bank.open_account(
                ask("Type (savings/current): "), ask("Name: "), ask("Email: "), ask("4-digit PIN: ")
            )
            say(f"Opened {acc.kind} account #{acc.number}")
        elif c == "2":
            bank.close_account(int(ask("Account #: ")))
            say("Closed.")
        elif c == "3":
            for a in bank.accounts():
                say(f"#{a.number} {a.name:<15} {a.kind:<8} {a.balance}")
        elif c == "4":
            say(f"Total balance: {bank.total_balance()}  Total loans: {bank.total_loans()}")
        elif c == "5":
            bank.loans_enabled = not bank.loans_enabled
            say(f"Loans {'enabled' if bank.loans_enabled else 'disabled'}")


def customer_menu(bank: Bank, ask: Ask, say: Say) -> None:
    acc = bank.get(int(ask("Account #: ")))
    prompt = (
        "\n[Customer] 1) Deposit 2) Withdraw 3) Balance 4) History "
        "5) Loan 6) Transfer 7) Interest 8) Back: "
    )
    while (c := ask(prompt)) != "8":
        if c == "1":
            acc.deposit(Decimal(ask("Amount: ")))
        elif c == "2":
            acc.withdraw(Decimal(ask("Amount: ")))
        elif c == "3":
            say(f"Balance: {acc.balance}")
        elif c == "4":
            for t in acc.history:
                say(f"{t.at:%Y-%m-%d %H:%M} {t.kind:<12} {t.amount:>10} -> {t.balance_after}")
        elif c == "5":
            bank.grant_loan(acc.number, Decimal(ask("Amount: ")))
        elif c == "6":
            bank.transfer(acc.number, int(ask("To account #: ")), Decimal(ask("Amount: ")))
        elif c == "7":
            # isinstance check: only savings accounts earn interest.
            if isinstance(acc, SavingsAccount):
                say(f"Interest added: {acc.add_interest()}")
            else:
                say("Only savings accounts earn interest.")
        say(f"Balance: {acc.balance}")


def atm_menu(atm: ATM, ask: Ask, say: Say) -> None:
    atm.insert_card(int(ask("Card (account #): ")), ask("PIN: "))
    while (c := ask("\n[ATM] 1) Balance 2) Withdraw 3) Eject: ")) != "3":
        if c == "2":
            atm.withdraw(Decimal(ask("Amount: ")))
        say(f"Balance: {atm.balance()}")
    atm.eject()


def run(bank: Bank, ask: Ask = input, say: Say = print) -> None:
    atm = ATM(bank)
    while (c := ask("\n1) Admin 2) Customer 3) ATM 4) Exit: ")) != "4":
        menus = {
            "1": lambda: admin_menu(bank, ask, say),
            "2": lambda: customer_menu(bank, ask, say),
            "3": lambda: atm_menu(atm, ask, say),
        }
        try:
            menus.get(c, lambda: say("Choose 1-4."))()
        # One place to report every expected error type.
        except (BankError, ValueError, InvalidOperation) as err:
            say(f"Error: {err}")


def main() -> int:
    try:
        run(Bank("Practice Bank"))
    except (EOFError, KeyboardInterrupt):
        # Ctrl-D / Ctrl-C: leave cleanly instead of showing a traceback.
        print("\nGoodbye!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
