from .prompt_strategy import PromptStrategy


class BeginnerPromptStrategy(PromptStrategy):
    """
    Strategy for beginner-level prompts.
    """

    def generate_prompt(self, subject: str, language: str) -> dict:
        return {
            "system_message": """
                You are a programming teacher for beginners.
                Focus on creating simple and clear exercises to teach foundational concepts.""",
            "user_message": f"""
                You will write an exercise on the next subject {subject} in the language {language}.
                The exercise should match the difficulty level 'beginner'.
                Include:
                    - Instructions in comments like leetcode.
                    - Clear and detailed comments to guide the student step-by-step.
                    - A simple starter code that the student can complete with minimal effort.
                    - Only pure code (no markdown or backticks).
                    - The exercise should be solvable in less than 5 minutes. """
        }
