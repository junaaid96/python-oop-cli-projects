"""Tests for the quiz game."""

from quiz_game.game import Quiz, Result
from quiz_game.questions import MultipleChoiceQuestion, ShortAnswerQuestion, TrueFalseQuestion


def test_question_types() -> None:
    assert TrueFalseQuestion("x", answer=False).is_correct("false")
    assert MultipleChoiceQuestion("x", choices=["a", "b"], correct_index=1).is_correct("2")
    assert not MultipleChoiceQuestion("x", choices=["a"], correct_index=0).is_correct("abc")
    assert ShortAnswerQuestion("x", accepted=("Init",)).is_correct(" init ")


def test_quiz_scores_with_fake_input() -> None:
    questions = [
        TrueFalseQuestion("a", answer=True),
        MultipleChoiceQuestion("b", choices=["x", "y"], correct_index=0, points=2),
    ]
    # An iterator of scripted answers stands in for the keyboard.
    answers = iter(["yes", "2"])
    messages: list[str] = []
    result = Quiz(questions, shuffle=False).run(lambda _: next(answers), messages.append)
    assert result == Result(1, 3)
    assert messages == ["Correct!", "Wrong."]
    assert round(result.percent) == 33
