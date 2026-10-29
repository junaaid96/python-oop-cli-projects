# 05 · File Organizer (Beginner → Intermediate) · functional style

Sorts a messy folder into `images/`, `documents/`, `audio/`... Dry run by default.

**Concepts:** pure functions, immutability (`NamedTuple`, `frozenset`), "functional core, imperative shell", `pathlib`, `shutil`.

```bash
uv run file-organizer ~/Downloads          # preview
uv run file-organizer ~/Downloads --apply  # move
```

## Why functional here?
The job is a data transformation: *list of files → list of moves*. No long-lived state needs guarding, so plain functions are simpler than classes. See [docs/18_oop_vs_functional.md](../../docs/18_oop_vs_functional.md).

## Exercises
1. Add `--by-date` to sort into `YYYY/MM` folders using file modification time.
2. Load categories from a TOML file (`tomllib`).
3. Write an `undo` log (JSON) so the last run can be reversed.
4. Detect duplicates by hashing content (`hashlib`).
