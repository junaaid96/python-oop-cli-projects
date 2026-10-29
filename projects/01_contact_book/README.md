# 01 · Contact Book (Beginner)

Store contacts in a JSON file from the command line.

**Concepts:** classes, `@dataclass(frozen=True)`, validation in `__post_init__`, `pathlib`, JSON, `argparse` sub-commands, `match`.

```bash
uv run contact-book add "Ada Lovelace" "+1 555 0100" --email ada@example.com
uv run contact-book list
uv run contact-book search ada
uv run contact-book remove "Ada Lovelace"
```

## Design
- `Contact` is an immutable value object; it validates itself.
- `ContactBook` owns the collection and its persistence (load on start, `save()` after changes).
- `cli.py` only parses arguments and prints; no business logic lives there.

## Exercises
1. Add an `edit` command that updates a phone number (hint: `dataclasses.replace`).
2. Add tags/groups to contacts and a `--tag` filter on `list`.
3. Export to CSV with the `csv` module.
4. Validate emails with a small regular expression and test it.
