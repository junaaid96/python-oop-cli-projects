# 06 · Banking System + ATM (Intermediate) · migrated

Originally [`junaaid96/banking_system`](https://github.com/junaaid96/banking_system). Its git history is preserved in this repo.

**Concepts:** abstract base classes, encapsulation (`_protected`, `__private`, read-only `@property`), polymorphism (`withdraw_limit`), `Decimal` for money, factory registry, custom exceptions, fixtures in pytest.

```bash
uv run banking
```

## Features
- **Admin:** open/close accounts, list accounts, total balance, total loans, toggle loans.
- **Customer:** deposit, withdraw, balance, history, loan (max 2), transfer, savings interest.
- **ATM:** PIN login, lockout after 3 wrong PINs, cash in multiples of 10, ATM cash limit.

## What changed from the original
- No global `Account.total_accounts` list: a `Bank` object owns its accounts.
- Sequential account numbers instead of random ones that could collide.
- `Decimal` instead of `float`; errors are exceptions instead of returned strings.
- The original transfer only checked the first account in the list; now it looks up by number.
- Savings vs Current now actually behave differently (interest vs overdraft).

## Exercises
1. Persist the bank to SQLite (see project 07 for the pattern).
2. Add a monthly statement export to CSV.
3. Add daily withdrawal limits at the ATM.
4. Add loan repayment with interest and a schedule.
