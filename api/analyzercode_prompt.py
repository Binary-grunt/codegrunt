# HACK: Need to thinking about how to refactor this code to avoid duplication.

class AnalyzerCodePrompt:

    @staticmethod
    def generate_prompt(file_content: str) -> dict:
        return {

            "system_message": """You are an AI code evaluator. You will analyze code provided by the user,
                    assess if it meets the requirements described, and return either 'Result: True'
                    if the code fully meets the requirements, or 'Result: False' if it doesn't.
                    Be strict in your evaluation, as if you were running unit tests.
                    Do not explain your answer.""",
            "user_message": f"""
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
        }
