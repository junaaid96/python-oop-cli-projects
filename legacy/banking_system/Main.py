from Bank import *


def find_account(account_number):
    for account in Account.total_accounts:
        if account.account_number == account_number:
            return account
    return None


while True:
    print("\n1. Admin Login")
    print("2. User Menu")
    print("3. Exit\n")

    choice = input("Enter your choice: ")

    if choice == "1":
        while True:
            print("\n1. Create Account")
            print("2. Delete Account")
            print("3. List Accounts")
            print("4. Check Total Bank Balance")
            print("5. Check Total Loan Amount")
            print("6. Loan Feature")
            print("7. Exit\n")

            choice = input("Enter your choice: ")

            if choice == "1":
                name = input("Enter name: ")
                email = input("Enter email: ")
                address = input("Enter address: ")
                account_type = input(
                    "Enter account type (Savings or Current): ")
                Bank.create_account(name, email, address, account_type)
                print("Account created successfully.")

            elif choice == "2":
                account_number = int(
                    input("Enter the account number to delete: "))
                for account in Account.total_accounts:
                    if account.account_number == account_number:
                        print(Bank.delete_account(account))
                        break
                else:
                    print("Account not found.")

            elif choice == "3":
                accounts = Bank.account_list()
                if len(accounts) == 0:
                    print("Account List is empty!")
                for account in accounts:
                    print(
                        f"Account number: {account.account_number}, Name: {account.name}, Balance: {account.balance}")

            elif choice == "4":
                print(Bank.total_bank_balance())

            elif choice == "5":
                print(Bank.total_loan_amount())

            elif choice == "6":
                status = input("Turn (On/Off): ")
                if status == "On":
                    print(Bank.toggle_loan_feature(True))
                elif status == "Off":
                    print(Bank.toggle_loan_feature(False))
                else:
                    print("Invalid input.")

            elif choice == "7":
                break

            else:
                print("Invalid choice.")

    elif choice == "2":
        while True:
            print("\n1. Create Account")
            print("2. Deposit")
            print("3. Withdraw")
            print("4. Check Balance")
            print("5. Transaction History")
            print("6. Take Loan")
            print("7. Transfer Amount")
            print("8. Exit\n")

            choice = input("Enter your choice: ")

            if choice == "1":
                name = input("Enter name: ")
                email = input("Enter email: ")
                address = input("Enter address: ")
                account_type = input(
                    "Enter account type (Savings or Current): ")
                Bank.create_account(name, email, address, account_type)
                print(
                    f"Account created successfully.")

            elif choice == "2":
                account_number = int(input("Enter your account number: "))
                amount = float(input("Enter the amount to deposit: "))
                account = find_account(account_number)
                if account:
                    print(account.deposit(amount))
                else:
                    print("Account not found.")

            elif choice == "3":
                account_number = int(input("Enter your account number: "))
                amount = float(input("Enter the amount to withdraw: "))
                account = find_account(account_number)
                if account:
                    print(account.withdraw(amount))
                else:
                    print("Account not found.")

            elif choice == "4":
                account_number = int(input("Enter your account number: "))
                account = find_account(account_number)
                if account:
                    print(account.check_balance())
                else:
                    print("Account not found.")

            elif choice == "5":
                account_number = int(input("Enter your account number: "))
                account = find_account(account_number)
                if account:
                    transactions = account.transaction_history()
                    for transaction in transactions:
                        print(transaction)
                else:
                    print("Account not found.")

            elif choice == "6":
                account_number = int(input("Enter your account number: "))
                loan_amount = float(input("Enter the loan amount: "))
                account = find_account(account_number)
                if account:
                    print(account.take_loan(loan_amount))
                else:
                    print("Account not found.")

            elif choice == "7":
                account_number = int(input("Enter your account number: "))
                other_account_number = int(
                    input("Enter the recipient's account number: "))
                amount = float(input("Enter the amount to transfer: "))
                account = find_account(account_number)
                other_account = find_account(other_account_number)
                if account and other_account:
                    print(account.transfer_amount(other_account, amount))
                elif not account:
                    print("Your account not found.")
                else:
                    print("Recipient account not found.")

            elif choice == "8":
                break
            else:
                print("Invalid choice.")
    else:
        break
