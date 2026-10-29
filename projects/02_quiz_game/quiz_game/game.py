"""The quiz engine. It depends only on the abstract `Question` type."""

from __future__ import annotations

import random

# Callable describes "a function"; we inject input/output for easy testing.
from collections.abc import Callable
from dataclasses import dataclass

from quiz_game.questions import (
    MultipleChoiceQuestion,
    Question,
    ShortAnswerQuestion,
    TrueFalseQuestion,
)


@dataclass
class Result:
    score: int
    total: int

    # @property exposes a computed value like an attribute: result.percent
    @property
    def percent(self) -> float:
        return 100 * self.score / self.total if self.total else 0.0


class Quiz:
    def __init__(self, questions: list[Question], shuffle: bool = True) -> None:
        # Copy the list so shuffling never changes the caller's list.
        self._questions = list(questions)
        if shuffle:
            random.shuffle(self._questions)

    def run(self, ask: Callable[[str], str], say: Callable[[str], None]) -> Result:
        score = 0
        # sum() of a generator: total possible points.
        total = sum(q.points for q in self._questions)
        for number, question in enumerate(self._questions, start=1):
            # Polymorphism: render()/is_correct() run the subclass's version.
            reply = ask(f"\nQ{number}. {question.render()}\n> ")
            if question.is_correct(reply):
                score += question.points
                say("Correct!")
            else:
                say("Wrong.")
        return Result(score, total)


def default_questions() -> list[Question]:
    # A small built-in question bank about Python itself.
    return [
        TrueFalseQuestion("Python lists are mutable.", answer=True),
        TrueFalseQuestion("A tuple can be changed after creation.", answer=False),
        MultipleChoiceQuestion(
            "Which keyword defines a class?", choices=["def", "class", "struct"], correct_index=1
        ),
        MultipleChoiceQuestion(
            "Which decorator makes a method readable like an attribute?",
            choices=["@staticmethod", "@property", "@classmethod"],
            correct_index=1,
            points=2,
        ),
        ShortAnswerQuestion(
            "Name the method that initializes a new object.", accepted=("__init__",)
        ),
    ]
