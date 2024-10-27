import os
from file_generators.file_and_directory_manager import create_directory, generate_file_path
from core_utils.openai_helpers import generated_exercice
from config import LANGUAGE_EXTENSIONS, set_current_exercise_path, FILE_EXTENSION_MAP


def write_exercise_to_file(file_path: str, content: str) -> str:
    """Writes the generated content to a file at the specified path."""
    with open(file_path, "w") as generated_file:
        generated_file.write(content)

    print(f"File '{file_path}' generated successfully in '{
          os.path.dirname(file_path)}'.")
    return file_path


def create_exercise_file(lang: str, subject: str, directory_path: str) -> str:
    """Creates an exercise file for the specified subject and language."""
    lang = lang.lower()

    if lang in LANGUAGE_EXTENSIONS:
        extension, language_name = LANGUAGE_EXTENSIONS[lang]

        # Create the directory if it does not exist
        create_directory(directory_path)

        # Generate the exercise and determine the file path
        try:
            exercise_content = generated_exercice(subject, language_name)
            file_path = generate_file_path(directory_path, lang, extension)

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


def generate_new_exercise(file_path: str) -> None:
    directory, original_filename = os.path.split(file_path)
    _, extension = os.path.splitext(original_filename)
    lang = FILE_EXTENSION_MAP.get(extension[1:].lower())

    if lang is None:
        print(f"Invalid language '{
              extension[1:]}'. Please select a valid language.")
        return

    # Increment the file number and generate a new exercise
    new_file_path = create_exercise_file(
        lang, subject=lang, directory_path=directory)

    if new_file_path:
        set_current_exercise_path(new_file_path)
        print("New exercise generated. Check your directory for the new file.")
        print(f"Your current exercise is: {new_file_path}.")
    else:
        print("Failed to generate a new exercise.")
