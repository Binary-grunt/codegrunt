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
                    - Write just prototype starter code that the student can complete.
                    - Provide only the function prototypes, structure, or necessary definitions (e.g., class/struct definitions).
                    - Do not write any logic, implementation, or completed code in the solution.
                    - Only pure code (no markdown or backticks) no explanation.
                    - The exercise should be solvable in less than 20 minutes. """
        }
