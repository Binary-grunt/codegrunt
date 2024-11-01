from file_generators.exercise_generator import create_exercise_file
from core_utils.path_manager import DirectoryManager, PathManager
from config.language_options import LANGUAGES
from cli.inputs import Inputs
import os


def generate_command(cli_inputs: Inputs) -> None:
    path_manager = PathManager()
    lang_choice = cli_inputs.get_language_choice()
    lang = LANGUAGES[lang_choice]
    subject = cli_inputs.get_subject()

    if lang and subject:

        # Determine the directory path for the exercise
        full_directory_path = DirectoryManager.directory_path(subject, lang)

        # Generate the exercise file and determine the file path
        file_path = create_exercise_file(lang, subject, full_directory_path)
        # Start the session and get the language and subject

        if file_path:
            # Set the current exercise path
            path_manager.set_current_exercise_path(file_path)
            # Extract just the filename from the full path
            path_manager.show_current_exercise()
        else:
            print("Failed to generate the exercise file.")
    else:
        print("Failed to generate command due to invalid input.")
