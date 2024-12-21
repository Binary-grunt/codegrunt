from openai import OpenAI


class OpenAIPrompt:
    """
    A class to manage prompts and interact with OpenAI.
    """
    DEFAULT_MODEL = "gpt-4o-mini"  # Default model for OpenAI interactions

    def __init__(self, client: OpenAI, model: str = None):
        """
        Initializes the OpenAIPrompt instance with a given OpenAI client.
        """
        self.client = client
        self.model = model or self.DEFAULT_MODEL

    def _generate_message(self, role: str, content: str) -> dict:
        """
        Helper method to create a message dictionary for OpenAI.

        Args:
            role (str): The role of the message ("system", "user", etc.).
            content (str): The content of the message.

        Returns:
            dict: The message dictionary.
        """
        return {"role": role, "content": content}

    def generate_exercise(self, subject: str, language: str) -> str:
        """
        Creates a chat completion based on the given subject and language.

        Args:
            subject (str): The programming subject for the exercise.
            language (str): The programming language for the exercise.

        Returns:
            str: The generated exercise code.
        """
        system_message = """You are a programming teacher. Create simple exercises with instructions in comments."""
        user_message = f"""
                        Write will create a exercice on the next subject {subject} on the language {language}
                        and make a exercice simple to create variable in programming, just the code without
                        markdown and ``` return pur code exercice. Just the instruction inside commentary
                        and the prototype code starter, like leetcode."""
        messages = [
            self._generate_message("system", system_message),
            self._generate_message("user", user_message),
        ]
        try:
            completion = self.client.chat.completions.create(model=self.model, messages=messages)
            return completion.choices[0].message.content
        except Exception as e:
            return f"An error occurred: {e}"

    def analyze_code(self, file_content: str) -> str:
        """
        Analyzes the provided code to determine if it meets the given requirements.

        Args:
            file_content (str): The code to analyze.

        Returns:
            str: "Result: True" if the code meets the requirements, otherwise "Result: False".
        """
        system_message = """You are an AI code evaluator. You will analyze code provided by the user,
                    assess if it meets the requirements described, and return either 'Result: True'
                    if the code fully meets the requirements, or 'Result: False' if it doesn't.
                    Be strict in your evaluation, as if you were running unit tests.
                    Do not explain your answer."""
        user_message = f"""
                    Analyze the provided code to determine if it correctly follows the given instructions.
                    The code must:
                    1. Strictly follow the provided instructions.
                    2. Handle typical and edge cases effectively.
                    3. Be syntactically correct and execute as expected.
                    4. Implement the required logic accurately.
                    5. Return correct results for all input cases, similar to a real-world unit test.
                    If the code passes these criteria, return 'Result: True'. Otherwise, return 'Result: False'.
                    Here is the code:

                    {file_content}
                    Do not explain your reasoning or generate any text beyond 'Result: True' or 'Result: False'.
                    """
        messages = [
            self._generate_message("system", system_message),
            self._generate_message("user", user_message),
        ]

        try:
            completion = self.client.chat.completions.create(model=self.model, messages=messages)
            return completion.choices[0].message.content
        except Exception as e:
            return f"An error occurred: {e}"
