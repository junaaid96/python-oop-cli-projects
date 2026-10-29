# 12 · Designing Command-Line Apps

Two styles appear in this repo:

| Style | Good for | Examples |
|---|---|---|
| Interactive menu loop | games, learning, step-by-step flows | 02, 04, 06, 11 |
| `argparse` subcommands | scripting, automation, pipes | 03, 05, 07, 10, 14 |

```python
import argparse


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="todo")
    sub = parser.add_subparsers(dest="command", required=True)
    add = sub.add_parser("add")
    add.add_argument("title")
    add.add_argument("--priority", choices=["low", "high"], default="low")
    args = parser.parse_args(argv)  # argv=None reads sys.argv; tests pass a list
    ...
    return 0  # exit code: 0 ok, non-zero error


if __name__ == "__main__":
    raise SystemExit(main())
```

## Principles
- Keep the CLI thin: parse input → call the domain → format output.
- Errors go to the user as one clear line, with a non-zero exit code.
- Destructive actions default to a **dry run** (see 05 File Organizer).
- Store user data under `~/.python-oop-cli/`, never next to the code.
