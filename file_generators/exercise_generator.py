import os
from core_utils.path_manager import DirectoryManager, PathManager
from api.openai_helpers import OpenAIHelpers
from config.language_options import LANGUAGE_EXTENSIONS, FILE_EXTENSION_MAP


def write_exercise_to_file(file_path: str, content: str) -> str:
    """Writes the generated content to a file at the specified path."""
    with open(file_path, "w") as generated_file:
        generated_file.write(content)

    print(f"File '{file_path}' generated successfully in '{
          os.path.dirname(file_path)}'.")
    return file_path


def create_exercise_file(lang: str, subject: str, directory_path: str) -> str | None:
    """Creates an exercise file for the specified subject and language."""
    lang = lang.lower()
    open_ai_api = OpenAIHelpers()

    if lang in LANGUAGE_EXTENSIONS:
        extension, language_name = LANGUAGE_EXTENSIONS[lang]

        # Create the directory if it does not exist
        DirectoryManager.create_directory(directory_path)

        # Generate the exercise and determine the file path
        try:
            exercise_content = open_ai_api.generated_exercice(
                subject, language_name)
            file_path = PathManager.generate_file_path(
                directory_path, lang, extension)

            # Write the exercise to the file
            print(f"{language_name} exercise file generated successfully in '{
                  directory_path}'.")
            return write_exercise_to_file(file_path, exercise_content)

        except Exception as e:
            print(f"An error occurred while generating the exercise file: {e}")
            return None
    else:
        print(f"Invalid language '{lang}'. Please select a valid language.")
        return None


def generate_new_exercise(file_path: str, subject: str) -> None:
    directory, original_filename = os.path.split(file_path)
    _, extension = os.path.splitext(original_filename)
    lang = FILE_EXTENSION_MAP.get(extension[1:].lower())

    if lang is None:
        print(f"Invalid language '{
              extension[1:]}'. Please select a valid language.")
        return

    # Increment the file number and generate a new exercise
    new_file_path = create_exercise_file(
        lang, subject, directory_path=directory)

    if new_file_path:
        PathManager.set_current_exercise_path(new_file_path)
        print(f"New exercise generated. On subject {
              subject}Check your directory for the new file.")
        print(f"Your current exercise is: {new_file_path}.")
    else:
        print("Failed to generate a new exercise.")
