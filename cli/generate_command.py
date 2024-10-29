from file_generators.exercise_generator import create_exercise_file
from core_utils.path_manager import DirectoryManager, PathManager
from config.language_options import LANGUAGES
from cli_inputs import CLIInputs
import os


def generate_command(cli_inputs: CLIInputs) -> None:
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
        # cli_inputs.start_session()
        print(f"File generated at: {file_path}")

        if file_path:
            # Set the current exercise path
            path_manager.set_current_exercise_path(file_path)
            print(f"Current exercise path set to: {file_path}")

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
