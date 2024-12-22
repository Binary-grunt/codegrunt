from .prompt_strategy import PromptStrategy


class IntermediatePromptStrategy(PromptStrategy):
    """
    Strategy for intermediate-level prompts.
    """

    def generate_prompt(self, subject: str, language: str) -> dict:
        return {
            "system_message": """
                You are a programming teacher for intermediate learners.
                Create exercises that build on foundational concepts with moderate complexity.""",
            "user_message": f"""
                You will write an exercise on the next subject {subject} in the language {language}.
                The exercise should match the difficulty level 'intermediate'.
                Include:
                    - Instructions in comments like leetcode.
                    - A starter code prototype that includes some pre-written structures.
                    - Only pure code (no markdown or backticks).
                    - The exercise should be solvable in 10-20 minutes, requiring some logical thinking.
                """
        }
