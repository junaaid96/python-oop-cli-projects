"""Play through the game in tests."""

from pathlib import Path

from text_adventure.cli import play
from text_adventure.commands import handle
from text_adventure.world import GameState, new_game

WALKTHROUGH = [
    "take lamp",
    "up",
    "take key",
    "d",
    "e",
    "take note",
    "read note",
    "n",
    "take trophy",
]


def test_walkthrough_wins() -> None:
    state = new_game()
    replies = [handle(state, line) for line in WALKTHROUGH]
    assert state.won and replies[-1].startswith("You lift the trophy")


def test_puzzles_block_progress() -> None:
    state = new_game()
    handle(state, "up")
    assert "too dark" in handle(state, "take key")
    handle(state, "down")
    handle(state, "east")
    assert "locked" in handle(state, "north")
    assert handle(state, "dance").startswith("Commands:")


def test_save_and_load(tmp_path: Path) -> None:
    script = iter(["take lamp", "save", "quit"])
    out: list[str] = []
    save = tmp_path / "s.json"
    play(new_game(), lambda _: next(script), out.append, save)
    restored = GameState.load(save)
    assert restored.inventory == ["lamp"]
    assert "lamp" not in restored.room.items
