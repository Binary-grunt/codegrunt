from file_generators.exercise_generator import generate_new_exercise
from core_utils.openai_helpers import analyze_code
from core_utils.score_manager import score_count, has_been_evaluated, mark_as_evaluated
from config import get_current_exercise_path


def get_analyzed_code(file_path: str) -> str:
    with open(file_path, 'r') as file:
        code = file.read()
    return analyze_code(code)


def submit_command(global_score: dict) -> str:
    file_path = get_current_exercise_path()

    # Ensure the file path matches the current exercise file
    if not file_path:
        print("No current exercise to submit. Please generate an exercise first.")
        return
    try:

        if has_been_evaluated(file_path):
            print(f"The file '{
                  file_path}' has already been evaluated. You cannot evaluate it again.")
            return

        # Analyze file code provided
        result = get_analyzed_code(file_path)

        # Calculate the score with score_count function
        score_count(result, global_score)
        mark_as_evaluated(file_path)

        # Generate a new exercise on the same subject
        generate_new_exercise(file_path)

    except FileNotFoundError:
        print(f"Error: The file '{
            file_path}' was not found. Please check the file path and try again.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
