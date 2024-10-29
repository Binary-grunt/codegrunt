from file_generators.exercise_generator import generate_new_exercise
from api.openai_helpers import OpenAIHelpers
from core_utils.score_manager import ScoreManager
from core_utils.path_manager import PathManager
from cli_inputs import CLIInputs


def submit_command(score: ScoreManager, cli_inputs: CLIInputs) -> str:
    open_ai_api = OpenAIHelpers()
    path = PathManager()
    file_path = path.get_current_exercise_path()
    print("______________________\n")
    print(f"Path : {file_path}")

    # Ensure the file path matches the current exercise file
    if not file_path:
        print("No current exercise to submit. Please generate an exercise first.")
        return
    try:

        if score.has_been_evaluated(file_path):
            print(f"The file '{
                  file_path}' has already been evaluated. You cannot evaluate it again.")
            return

        # Analyze file code provided
        result = open_ai_api.get_analyzed_code(file_path)

        # Calculate the score with score_count function
        score.score_count(result)
        score.mark_as_evaluated(file_path)

        # Generate a new exercise on the same subject
        generate_new_exercise(file_path, cli_inputs.subject)

    except FileNotFoundError:
        print(f"Error: The file '{
            file_path}' was not found. Please check the file path and try again.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
