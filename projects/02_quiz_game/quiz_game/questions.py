"""Question types. Each subclass answers `is_correct` its own way (polymorphism)."""

from __future__ import annotations

# ABC + abstractmethod: a base class that cannot be instantiated on its own.
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class Question(ABC):
    prompt: str
    # Points awarded for a correct answer; subclasses inherit this field.
    points: int = 1

    @abstractmethod
    def is_correct(self, answer: str) -> bool:
        """Every concrete question must decide how to check an answer."""

    def render(self) -> str:
        # Default rendering; subclasses may override (method overriding).
        return self.prompt


@dataclass
class TrueFalseQuestion(Question):
    answer: bool = True

    def is_correct(self, answer: str) -> bool:
        # Accept t/true/y/yes as True; anything else counts as False.
        return (answer.strip().lower() in {"t", "true", "y", "yes"}) == self.answer

    def render(self) -> str:
        # super() calls the parent version, then we add a hint.
        return f"{super().render()} (true/false)"


@dataclass
class MultipleChoiceQuestion(Question):
    # field(default_factory=list) avoids the shared-mutable-default bug.
    choices: list[str] = field(default_factory=list)
    correct_index: int = 0

    def is_correct(self, answer: str) -> bool:
        # The user types a 1-based number; convert safely.
        return answer.strip().isdigit() and int(answer) - 1 == self.correct_index

    def render(self) -> str:
        lines = [self.prompt]
        # enumerate(start=1) gives "1) ..., 2) ..." numbering.
        lines += [f"  {i}) {choice}" for i, choice in enumerate(self.choices, start=1)]
        return "\n".join(lines)


@dataclass
class ShortAnswerQuestion(Question):
    # Several spellings may be accepted.
    accepted: tuple[str, ...] = ()

    def is_correct(self, answer: str) -> bool:
        # casefold() is a stronger lower() for case-insensitive comparison.
        return answer.strip().casefold() in {a.casefold() for a in self.accepted}
