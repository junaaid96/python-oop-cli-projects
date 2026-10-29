# 03 · Todo Manager (Beginner)

A persistent task list with priorities, due dates and tags.

**Concepts:** `StrEnum`, `datetime.date`, `@classmethod` alternative constructors, the repository pattern, keyword-only arguments, JSON persistence.

```bash
uv run todo add "Read docs/04_polymorphism.md" --priority high --due 2026-12-01 --tag study
uv run todo list
uv run todo done 1
uv run todo list --all
```

## Exercises
1. Swap `TaskRepository` for a `SqliteTaskRepository` with the same methods (see project 07).
2. Add recurring tasks (daily/weekly) that re-create themselves when completed.
3. Add an `edit` command and an undo stack (Command pattern).
4. Show a summary: counts per priority and overdue tasks.
