from abc import ABC, abstractmethod


class PromptStrategy(ABC):
    """
    Base class for all prompt generation strategies.
    """

    @abstractmethod
    def generate_prompt(self, subject: str, language: str) -> dict:
        """
        Generates the system and user prompts based on the strategy.

        Args:
            subject (str): The programming subject.
            language (str): The programming language.

        Returns:
            dict: A dictionary with "system_message" and "user_message".
        """
        pass
