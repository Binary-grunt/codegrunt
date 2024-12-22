from .prompt_strategy import PromptStrategy


class ExpertPromptStrategy(PromptStrategy):
    """
    Strategy for expert-level prompts.
    """

    def generate_prompt(self, subject: str, language: str) -> dict:
        return {
            "system_message": """
                You are a programming teacher for expert learners.
                Create highly complex exercises that challenge the student's mastery of advanced programming concepts.""",
            "user_message": f"""
                You will write an exercise on the next subject {subject} in the language {language}.
                The exercise should match the difficulty level 'expert'.
                Include:
                    - Instructions in comments like leetcode.
                    - Minimal comments to describe the high-level objective, leaving the rest to the student's interpretation.
                    - A starter code that only initializes the environment, with the student needing to build the entire solution.
                    - Only pure code (no markdown or backticks).
                    - The exercise should be solvable in 30-50 minutes and demand in-depth knowledge and creativity.
                """
        }
