from Account import *


class Bank:
    @staticmethod
    def create_account(name, email, address, account_type):
        if account_type == "Savings":
            return SavingsAccount(name, email, address)
        elif account_type == "Current":
            return CurrentAccount(name, email, address)
        else:
            return "Invalid account type!"

    @staticmethod
    def delete_account(account):
        if account in Account.total_accounts:
            Account.total_accounts.remove(account)
            del account
            return "Account deleted successfully!"
        else:
            return "Account not found!"

    @staticmethod
    def account_list():
        return Account.total_accounts

    @staticmethod
    def total_bank_balance():
        total_balance = sum(
            account.balance for account in Account.total_accounts)
        return f"Total bank balance: {total_balance}"

    @staticmethod
    def total_loan_amount():
        total_loan = sum(loan.loan for loan in Account.total_accounts)
        return f"Total loan amount granted: {total_loan}"

    @staticmethod
    def toggle_loan_feature(status):
        Account.loan_feature_enabled = status
        return f"Loan feature is {'enabled' if status else 'disabled'}."
