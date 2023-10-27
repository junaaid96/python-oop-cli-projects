import random


class Account:
    total_accounts = []
    loan_feature_enabled = True

    def __init__(self, name, email, address, account_type) -> None:
        self.name = name
        self.email = email
        self.address = address
        self.account_type = account_type
        self.account_number = random.randint(1000, 2000)
        self.balance = 0
        self.deposited = 0
        self.transactions = []

        Account.total_accounts.append(self)

    def deposit(self, amount):
        if amount >= 0:
            self.balance += amount
            self.deposited += amount
            self.transactions.append(f"Deposited: {amount}")
            return f"{amount} deposited. Current balance: {self.balance}"
        else:
            return "Invalid amount"

    def withdraw(self, amount):
        if amount < 0:
            return "Invalid amount"
        elif self.balance >= amount:
            self.balance -= amount
            return f"{amount} withdrawn. Current balance: {self.balance}"
        elif self.deposited == amount:
            return "Your bank is bankrupt"
        else:
            return "Withdrawal amount exceeded!"

    def check_balance(self):
        return f"Available balance: {self.balance}"

    def transaction_history(self):
        return self.transactions

    def take_loan(self, loan_amount):
        if Account.loan_feature_enabled:
            if len(self.transactions) < 2 and loan_amount > 0:
                self.balance += loan_amount
                self.transactions.append(f"Loan taken: {loan_amount}")
                return f"Loan {loan_amount} added. Current balance: {self.balance}"
            else:
                return "Loan limit exceed."
        else:
            return "Loan feature is disabled."

    def transfer_amount(self, other_account, amount):
        for account in Account.total_accounts:
            if (account == other_account):
                if self.balance >= amount:
                    self.balance -= amount
                    other_account.balance += amount
                    self.transactions.append(
                        f"Transferred {amount} to Account {other_account.account_number}")
                    return f"Transferred {amount} to Account {other_account.account_number}. Current balance: {self.balance}"
                else:
                    return "Insufficient balance."
            else:
                return "Account does not exist!"


class SavingsAccount(Account):
    def __init__(self, name, email, address) -> None:
        super().__init__(name, email, address, "Savings")


class CurrentAccount(Account):
    def __init__(self, name, email, address) -> None:
        super().__init__(name, email, address, "Current")

