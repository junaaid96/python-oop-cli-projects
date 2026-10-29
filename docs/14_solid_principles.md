# 14 · SOLID Principles in Python

| Principle | One-liner | In this repo |
|---|---|---|
| **S**ingle Responsibility | one reason to change | 13 Hotel splits domain / repository / service / CLI |
| **O**pen/Closed | add behaviour by adding code, not editing it | 09 pricing strategies, 12 discounts, 15 command registry |
| **L**iskov Substitution | subclasses must work wherever the parent does | 06 account types |
| **I**nterface Segregation | small, focused interfaces | 14 `LinkStore` Protocol has 4 methods |
| **D**ependency Inversion | depend on abstractions, inject concretes | 14 `Shortener(store)`, every `cli.py` takes `ask/say` |

```python
# Before: the report knows about the database AND formatting AND email.
# After: each concern is its own object, wired together at the edge.
report = Report(repo=SqliteExpenseRepo(path), formatter=MarkdownFormatter())
```

Don't apply SOLID ceremonially. A 30-line script needs none of it. Apply it when code starts to hurt to change.
