import os
from files_generated import create_file
from openai_helpers import analyze_code
from score_manager import score_count, has_been_evaluated, mark_as_evaluated


def generate_command():
    print("Please select the language -\n"
          "1. PHP\n"
          "2. JavaScript\n"
          "3. Python\n")

    lang_choice = input(
        "What's the programming language you want to learn? ")

    if lang_choice in ['1', '2', '3']:
        subject = input("What's the subject you want to practice? ")

        languages = {
            '1': 'PHP',
            '2': 'JavaScript',
            '3': 'Python',
        }
        lang = languages[lang_choice]
        if lang and subject:
            create_file(lang, subject)
        else:
            print("The language or subject is invalid.")
    else:
        print("Invalid language selection. Please enter 1, 2, or 3.")


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
