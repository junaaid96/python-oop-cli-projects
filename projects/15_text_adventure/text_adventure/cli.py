"""Play: `text-adventure [--load FILE]`. Type `save` or `quit` any time."""

import argparse
from collections.abc import Callable, Sequence
from pathlib import Path

from text_adventure.commands import handle
from text_adventure.world import GameState, new_game

SAVE = Path.home() / ".python-oop-cli" / "adventure.json"


def play(
    state: GameState, ask: Callable[[str], str], say: Callable[[str], None], save_to: Path
) -> None:
    say(handle(state, "look"))
    while not state.won:
        line = ask("> ").strip().lower()
        if line in {"quit", "q"}:
            return
        if line == "save":
            save_to.parent.mkdir(parents=True, exist_ok=True)
            state.save(save_to)
            say(f"Saved to {save_to}")
            continue
        say(handle(state, line))


def main(argv: Sequence[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="text-adventure")
    p.add_argument("--load", type=Path, help="continue a saved game")
    p.add_argument("--save-file", type=Path, default=SAVE)
    args = p.parse_args(argv)
    state = GameState.load(args.load) if args.load else new_game()
    play(state, input, print, args.save_file)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
