"""Imperative shell: reads the folder, calls the pure core, then (optionally) moves files."""

import argparse
import shutil
from collections.abc import Sequence
from pathlib import Path

from file_organizer.core import plan_moves, resolve_conflicts, summarize


def organize(folder: Path, apply: bool) -> list[str]:
    files = [p for p in folder.iterdir() if p.is_file()]
    # rglob collects files already inside category folders to avoid overwriting them.
    existing = frozenset(p for p in folder.rglob("*") if p.is_file())
    moves = resolve_conflicts(plan_moves(files, folder), existing)
    lines = [f"{m.source.name} -> {m.target.relative_to(folder)}" for m in moves]
    if apply:
        for m in moves:
            Path(m.target).parent.mkdir(exist_ok=True)
            shutil.move(m.source, m.target)
    lines += [f"{cat}: {count}" for cat, count in summarize(moves).items()]
    return lines


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="file-organizer", description="Sort files by type.")
    parser.add_argument("folder", type=Path)
    # Safe by default: nothing moves unless --apply is given (a "dry run").
    parser.add_argument("--apply", action="store_true", help="actually move the files")
    args = parser.parse_args(argv)
    if not args.folder.is_dir():
        print(f"Error: {args.folder} is not a folder")
        return 1
    for line in organize(args.folder, args.apply):
        print(line)
    if not args.apply:
        print("(dry run - add --apply to move files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
