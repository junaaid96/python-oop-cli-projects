# 15 · Text Adventure (Advanced)

A small puzzle adventure: find the light, the key and the trophy.

**Concepts:** Command pattern with a registry, `ClassVar`, data-driven design (rooms are data), game state, JSON save/load with nested dataclasses.

```bash
uv run text-adventure
uv run text-adventure --load ~/.python-oop-cli/adventure.json
```

Type `look`, `go east` (or just `e`), `take lamp`, `inventory`, `read note`, `save`, `quit`.

## Exercises
1. Load the whole world from a JSON file so non-programmers can design maps.
2. Add `drop`, `use` and an NPC with a dialogue tree (State pattern).
3. Add `undo` by storing a stack of previous states (Memento pattern).
4. Add a rules-based hint bot: map keywords in the player's question to hints.
