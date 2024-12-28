from .prompt_strategy import PromptStrategy


class AdvancedPromptStrategy(PromptStrategy):
    """
    Strategy for advanced-level prompts.
    """

    def generate_prompt(self, subject: str, language: str) -> dict:
        return {
            "system_message": """
            You are a programming teacher for advanced learners.
            Create challenging exercises that require problem-solving skills and advanced concepts.""",
            "user_message": f"""
                You will write an exercise on the next subject {subject} in the language {language}.
                Do not write the solution code.
                The exercise should match the difficulty level 'advanced'.
                Include:
                    - Instructions in comments like leetcode.
                    - Brief comments to outline the problem, leaving the student to infer the solution logic.
                    - Starter code that sets up a complex problem, but requires significant completion by the student.
                    - Only pure code (no markdown or backticks).
                    - The exercise should be solvable in 20-30 minutes and encourage critical thinking.
                """
        }
