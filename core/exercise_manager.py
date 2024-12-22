from api.factories.prompt_exercise_factory import PromptExerciseFactory
from api.analyzercode_prompt import AnalyzerCodePrompt
from api.openai_service import OpenAIService


class ExerciseManager:
    """
    Manages the interaction between the user and the OpenAI API to generate exercises and analyze code.
    """

    def __init__(self, openai_service: OpenAIService):
        self.openai_service = openai_service

    def execute_prompt(self, prompt: dict[str, str]) -> str:
        """
        Sends the prompt messages to the OpenAI API and returns the response.

        Args:
            prompt (dict): A dictionary containing "system_message" and "user_message".

        Returns:
            str: The response content from OpenAI.
        """
        messages = [
            {"role": "system", "content": prompt["system_message"]},
            {"role": "user", "content": prompt["user_message"]},
        ]
        return self.openai_service.request_response_to_openai(messages)

    def generate_exercise(self, subject: str, language: str, level: str) -> str:
        """
        Creates a chat completion based on the given subject, language, and difficulty level.

        Args:
            subject (str): The programming subject for the exercise.
            language (str): The programming language for the exercise.
            level (str): The difficulty level (e.g., "beginner", "intermediate", "advanced", "expert").

        Returns:
            str: The generated exercise code.
        """
        strategy = PromptExerciseFactory.create_prompt_exercise(level)
        prompt = strategy.generate_prompt(subject, language)
        return self.execute_prompt(prompt)

    def analyze_code(self, file_content: str) -> str:
        """
        Analyzes the provided code to determine if it meets the given requirements.

        Args:
            file_content (str): The code to analyze.

        Returns:
            str: "Result: True" if the code meets the requirements, otherwise "Result: False".
        """
        prompt = AnalyzerCodePrompt.generate_prompt(file_content)
        return self.execute_prompt(prompt)
