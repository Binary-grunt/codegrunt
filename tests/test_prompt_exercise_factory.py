import pytest
from api.factories.prompt_exercise_factory import PromptExerciseFactory
from api.strategies import (
    BeginnerPromptStrategy,
    IntermediatePromptStrategy,
    AdvancedPromptStrategy,
    ExpertPromptStrategy,
)


@pytest.mark.parametrize(
    "level, expected_class",
    [
        ("beginner", BeginnerPromptStrategy),
        ("intermediate", IntermediatePromptStrategy),
        ("advanced", AdvancedPromptStrategy),
        ("expert", ExpertPromptStrategy),
    ]
)
def test_prompt_exercise_factory(level, expected_class):
    """
    Test that the PromptExerciseFactory creates the correct strategy for each difficulty level.
    """
    strategy = PromptExerciseFactory.create_prompt_exercise(level)
    assert isinstance(strategy, expected_class)


def test_prompt_exercise_factory_invalid_level():
    """
    Test that the PromptExerciseFactory raises an error for an invalid level.
    """
    with pytest.raises(ValueError, match="Unknown difficulty level: invalid"):
        PromptExerciseFactory.create_prompt_exercise("invalid")
