"""Run the quiz: `quiz-game [--no-shuffle]`."""

import argparse
from collections.abc import Sequence

from quiz_game.game import Quiz, default_questions


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="quiz-game", description="A tiny Python quiz.")
    # store_true flags default to False and become True when given.
    parser.add_argument("--no-shuffle", action="store_true")
    args = parser.parse_args(argv)
    quiz = Quiz(default_questions(), shuffle=not args.no_shuffle)
    # Pass the real input/print functions; tests pass fakes instead.
    result = quiz.run(input, print)
    print(f"\nScore: {result.score}/{result.total} ({result.percent:.0f}%)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
