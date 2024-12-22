from api.strategies import (
    BeginnerPromptStrategy,
    IntermediatePromptStrategy,
    AdvancedPromptStrategy,
    ExpertPromptStrategy,
    PromptStrategy
)


class PromptExerciseFactory:
    """
    Factory for creating prompt generation strategies based on difficulty levels.
    """
    _strategy_map = {
        "beginner": BeginnerPromptStrategy,
        "intermediate": IntermediatePromptStrategy,
        "advanced": AdvancedPromptStrategy,
        "expert": ExpertPromptStrategy,
    }

    @staticmethod
    def create_prompt_exercise(level: str) -> PromptStrategy:
        """
        Creates a prompt generation strategy based on the given level.

        Args:
            level (str): The difficulty level (e.g., beginner, intermediate, advanced, expert).

        Returns:
            PromptStrategy: The corresponding strategy instance.

        Raises:
            ValueError: If the level is unknown.
        """
        strategy_class = PromptExerciseFactory._strategy_map.get(level.lower())
        if not strategy_class:
            raise ValueError(f"Unknown difficulty level: {level}")
        return strategy_class()
