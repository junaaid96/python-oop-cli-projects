"""`log-analyzer FILE [--errors] [--prefix /api]`"""

import argparse
from collections.abc import Callable, Sequence
from pathlib import Path

from log_analyzer.pipeline import (
    Entry,
    all_of,
    compose,
    parse,
    path_startswith,
    status_at_least,
    summary,
    where,
)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="log-analyzer", description="Summarize access logs.")
    parser.add_argument("file", type=Path)
    parser.add_argument("--errors", action="store_true", help="only status >= 400")
    parser.add_argument("--prefix", help="only paths starting with this")
    args = parser.parse_args(argv)
    if not args.file.is_file():
        print(f"Error: {args.file} not found")
        return 1
    # Build the filter list declaratively, then compose one pipeline.
    preds: list[Callable[[Entry], bool]] = []
    if args.errors:
        preds.append(status_at_least(400))
    if args.prefix:
        preds.append(path_startswith(args.prefix))
    pipeline = compose(where(all_of(*preds)))
    with args.file.open(encoding="utf-8") as fh:  # the file is read lazily, line by line
        for key, value in summary(pipeline(parse(fh))).items():
            print(f"{key:<10} {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
