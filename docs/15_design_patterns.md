# 15 · Design Patterns, the Pythonic Way

| Pattern | Problem it solves | Pythonic form | Project |
|---|---|---|---|
| Strategy | swap an algorithm | pass an object or simply a function | 09 pricing, 12 discounts |
| Command | turn actions into objects | class with `execute`, kept in a dict registry | 15 |
| Repository | hide storage details | class with `add/get/list` over SQL/JSON | 03, 07, 13 |
| Observer | notify listeners of events | list of callbacks | 12 low-stock alerts |
| Composite | treat a group like an item | object holding children with same interface | 12 `BestOf` discount |
| Factory | choose which class to build | `@classmethod` or dict of classes | 03 `Task.from_dict`, 15 `GameState.load` |
| State | behaviour depends on state | enum + transitions, or state objects | 11 ride status, 13 bookings |
| Pipeline | chain transformations | generators | 10 Log Analyzer |
| Singleton | one shared instance | just use a module | — |

Many classic patterns shrink to a few lines in Python because functions are first-class objects. Use a pattern when it removes a real `if/elif` tangle, not to show it off.
