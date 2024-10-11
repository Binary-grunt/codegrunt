import os
from files_generated import create_file
from openai_helpers import analyze_code
from score_manager import score_count, has_been_evaluated, mark_as_evaluated


def evaluate_command(file_path: str, global_score: dict) -> str:
    try:
        if has_been_evaluated(file_path):
            print(f"The file '{
                  file_path}' has already been evaluated. You cannot evaluate it again.")
            return

        with open(file_path, 'r') as file:
            code = file.read()
        result = analyze_code(code)

        # Calculate the score with score_count function
        score_count(result, global_score)
        mark_as_evaluated(file_path)

        # HACK: Dont work
        # generare new subject
        subject, extension = os.path.splitext(file_path)
        lang = extension[1:]  # recup extension of the precedent exercice
        create_file(lang, subject)

    except FileNotFoundError:
        print(f"Error: The file '{
            file_path}' was not found. Please check the file path and try again.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
