# Banking System
banking system using python

## User Features

* **Account Creation**
  - Users can create an account by providing the following information:
    - Name
    - Email
    - Address
    - Account Type (Savings or Current)
  - Upon registration, the initial balance will be set to 0, and an account number will be automatically generated.

* **Deposit and Withdraw**
  - Users can deposit and withdraw money from their accounts. If a withdrawal amount exceeds the current balance, an error message will be displayed: "Withdrawal amount exceeded."

* **Check Balance**
  - Users can check their available account balance at any time.

* **Transaction History**
  - Users can view their transaction history to track their financial activities.

* **Loan Request**
  - Users can request a loan from the bank, but they can do this at most two times.

* **Account Transfer**
  - Users can transfer money from their account to another user's account. If the recipient's account does not exist, an error message will be displayed: "Account does not exist." Users can only withdraw and transfer money if they have a positive balance.

## Admin Features

* **Account Creation**
  - Admins can create new user accounts on behalf of customers.

* **Account Deletion**
  - Admins have the authority to delete user accounts if necessary.

* **View User Accounts**
  - Admins can see a list of all user accounts registered with the bank.

* **Total Bank Balance**
  - Admins can check the total available balance of the bank, which is the sum of all user account balances.

* **Total Loan Amount**
  - Admins can track the total loan amount granted by the bank.

* **Loan Feature Control**
  - Admins can toggle the loan feature on or off for the entire bank.
