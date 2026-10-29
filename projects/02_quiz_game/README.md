# 02 · Quiz Game (Beginner)

An interactive quiz with three question types.

**Concepts:** inheritance, abstract base classes, method overriding, `super()`, polymorphism, `@property`, dependency injection of `input`/`print` for testing.

```bash
uv run quiz-game
uv run quiz-game --no-shuffle
```

## Design
`Quiz` only knows the abstract `Question`. Adding a new question type never requires changing `Quiz` (Open/Closed principle).

## Exercises
1. Add a `NumericQuestion` that accepts answers within a tolerance.
2. Load questions from a JSON file (hint: a factory function keyed by `"type"`).
3. Add a timer per question and a high-score table saved to disk.
4. Add difficulty levels and choose questions by level.
