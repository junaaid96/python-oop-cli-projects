"""Pure functions need no setup; the shell is tested with a temporary folder."""

from pathlib import Path, PurePath

from file_organizer.cli import main
from file_organizer.core import Move, categorize, plan_moves, resolve_conflicts, summarize


def test_categorize() -> None:
    assert categorize(PurePath("a.PNG")) == "images"
    assert categorize(PurePath("notes")) == "other"


def test_plan_and_conflicts() -> None:
    root = PurePath("/r")
    moves = plan_moves([PurePath("/r/a.jpg"), PurePath("/r/.hidden")], root)
    assert moves == [Move(PurePath("/r/a.jpg"), PurePath("/r/images/a.jpg"))]
    fixed = resolve_conflicts(moves, frozenset({PurePath("/r/images/a.jpg")}))
    assert fixed[0].target.name == "a (1).jpg"
    assert summarize(fixed) == {"images": 1}


def test_cli_dry_run_and_apply(tmp_path: Path) -> None:
    (tmp_path / "song.mp3").write_text("x")
    assert main([str(tmp_path)]) == 0
    assert (tmp_path / "song.mp3").exists()  # dry run moved nothing
    assert main([str(tmp_path), "--apply"]) == 0
    assert (tmp_path / "audio" / "song.mp3").exists()
    assert main([str(tmp_path / "missing")]) == 1
