# 10 · SQLite with the Standard Library

```python
import sqlite3

db = sqlite3.connect("app.db")  # ":memory:" for tests
db.row_factory = sqlite3.Row  # rows behave like dicts
db.execute(
    "CREATE TABLE IF NOT EXISTS expense (id INTEGER PRIMARY KEY, amount TEXT, category TEXT)"
)

with db:  # commits, or rolls back on error
    db.execute("INSERT INTO expense (amount, category) VALUES (?, ?)", ("9.50", "food"))

for row in db.execute("SELECT category, COUNT(*) AS n FROM expense GROUP BY category"):
    print(row["category"], row["n"])
```

## Rules
- **Always use `?` placeholders.** Building SQL with f-strings allows SQL injection.
- Hide SQL behind a repository class so the rest of the app works with objects.
- Store money as TEXT/integer cents, never float.
- Add indexes for columns you filter on often.

**See it in:** 07 Expense Tracker, 13 Hotel, 14 URL Shortener.
