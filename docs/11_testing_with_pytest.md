# 11 · Testing with pytest

```python
import pytest


def test_withdraw_reduces_balance() -> None:  # name says the behaviour
    acc = Account(balance=100)  # Arrange
    acc.withdraw(30)  # Act
    assert acc.balance == 70  # Assert


def test_overdraw_raises() -> None:
    with pytest.raises(InsufficientFunds, match="need"):
        Account(balance=0).withdraw(1)


@pytest.mark.parametrize(("km", "fare"), [(0, 50), (10, 150)])
def test_fares(km: int, fare: int) -> None:
    assert price(km) == fare


@pytest.fixture
def repo(tmp_path):  # fresh setup per test
    return Repo(tmp_path / "db.json")
```

## Testing CLIs
Every `cli.py` in this repo takes `ask`/`say` callables instead of calling `input`/`print` directly, so tests feed scripted answers and collect output. `capsys` captures prints for argparse tools.

Run: `uv run pytest`, `uv run pytest -k banking -v`, `uv run pytest --lf` (last failures).

**See it in:** every `projects/*/tests/`. Project 14 runs one suite against two backends with a parametrized fixture.
