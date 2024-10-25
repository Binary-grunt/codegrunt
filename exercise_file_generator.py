from openai_helpers import generated_exercice
from config import LANGUAGE_EXTENSIONS
import os


def create_directory_if_not_exists(directory_name) -> str:
    """Create directory if not exist and return its name"""
    try:
        os.mkdir(directory_name)
        print(f"Directory '{directory_name}' created successfully.")
    except FileExistsError:
        print(f"Directory '{directory_name}' already exists.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{directory_name}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return directory_name


def generate_file_path(directory: str, subject: str, extension: str) -> str:
    """Generates a unique file path in the specified directory."""
    num = 0
    while True:
        file_name = f"{subject}_{num}.{extension}"
        file_path = os.path.join(directory, file_name)
        if not os.path.exists(file_path):
            return file_path  # Return the unique file path
        num += 1


def write_exercise_to_file(file_path: str, content: str) -> str:
    """Writes the generated content to a file at the specified path."""
    with open(file_path, "w") as generated_file:
        generated_file.write(content)

    print(f"File '{file_path}' generated successfully in '{
          os.path.dirname(file_path)}'.")
    return file_path


def create_exercise_file(lang: str, subject: str) -> str:
    """Creates an exercise file for the specified subject and language."""
    lang = lang.lower()

    if lang in LANGUAGE_EXTENSIONS:
        extension, language_name = LANGUAGE_EXTENSIONS[lang]

        # Create the directory for the subject and language
        directory_name = f"{subject}_{lang}"
        directory_path = create_directory_if_not_exists(directory_name)

        # Generate the exercise and determine the file path
        try:
            exercise_content = generated_exercice(subject, language_name)
            file_path = generate_file_path(directory_path, subject, extension)

            # Write the exercise to the file

            print(f"{language_name} exercise file generated successfully in '{
                  directory_path}'.")
            return write_exercise_to_file(file_path, exercise_content)

        except Exception as e:
            print(f"An error occurred while generating the exercise file: {e}")
            return None
    else:
        print("Invalid language. Please select a valid language.")
