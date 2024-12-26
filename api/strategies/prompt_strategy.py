from abc import ABC, abstractmethod


class PromptStrategy(ABC):
    """
    Base class for all prompt generation strategies.
    """

    @abstractmethod
    def generate_prompt(self, **kwargs) -> dict:
        """
        Generates the system and user prompts based on the strategy.

        Args:
            kwargs: Keyword arguments needed for generating the prompt.

        Returns:
            dict: A dictionary with "system_message" and "user_message".
        """
        pass
