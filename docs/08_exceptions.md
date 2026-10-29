# 08 · Exceptions and Error Handling

```python
class BankError(Exception):  # one base class per app/domain
    """Base for every banking error."""


class InsufficientFunds(BankError):
    def __init__(self, needed: int) -> None:
        super().__init__(f"need {needed} more")
        self.needed = needed


try:
    account.withdraw(500)
except InsufficientFunds as err:  # catch the most specific type you can handle
    print(err)
else:
    print("ok")  # runs only when no error happened
finally:
    log.flush()  # always runs
```

## Guidelines
- Raise in the **domain layer**; turn errors into friendly messages in the **CLI layer**.
- Never write a bare `except:`. Never silently `pass`.
- Use `raise NewError(...) from err` to keep the original cause.
- EAFP ("easier to ask forgiveness") is idiomatic: try it and catch `KeyError`, rather than pre-checking everything.
- `ExceptionGroup` / `except*` exist for concurrent errors.

**See it in:** 04 Ticket Booking, 06 Banking, 13 Hotel.
