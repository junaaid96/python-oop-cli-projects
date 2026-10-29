# 16 · Clean Code Habits

- **Names reveal intent:** `available_rooms`, not `lst2`. Booleans read as questions: `is_paid`.
- **Small functions** that do one thing; aim for under ~20 lines.
- **No magic numbers:** `LATE_FEE_PER_DAY = Decimal("0.50")`.
- **Guard clauses** instead of deep nesting: `if not x: return`.
- **Pure core, impure shell:** keep `input`, `print`, files and the clock at the edges.
- **Comments explain *why*.** The code shows *what*. (This repo over-comments on purpose to teach.)
- **Type hints + ruff + mypy** catch whole classes of bugs before you run anything.
- **Write the test first** when fixing a bug, so it can never come back.
- **Delete dead code.** Git remembers it.

Refactoring checklist: duplicated code → extract function; long parameter list → dataclass; type switch → polymorphism; global state → inject a dependency.
