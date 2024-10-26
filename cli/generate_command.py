from file_generators.exercise_generator import create_exercise_file, create_directory
from file_generators.file_and_directory_manager import directory_path
from config import LANGUAGES, set_current_exercise_path
from core_utils.cli_inputs import get_language_choice, get_subject
import os


def generate_command():
    lang_choice = get_language_choice()
    lang = LANGUAGES[lang_choice]
    subject = get_subject()

    if lang and subject:

        # Determine the directory path for the exercise
        full_directory_path = directory_path(subject, lang)

        # Generate the exercise file and determine the file path
        file_path = create_exercise_file(lang, subject, full_directory_path)
        print(f"File generated at: {file_path}")

        if file_path:
            # Set the current exercise path
            set_current_exercise_path(file_path)

            # Extract just the filename from the full path
            file_name = os.path.basename(file_path)
            print("______________________\n")
            print(f"Your current exercise is: {file_name}.\n")
            print("After completing it, use the 'submit' command to evaluate it.")
            print("______________________\n")
        else:
            print("Failed to generate the exercise file.")
    else:
        print("Failed to generate command due to invalid input.")
