import os


def create_directory(directory_name) -> str:
    """Create directory if not exist and return its name"""
    if not os.path.exists(directory_name):
        try:
            os.mkdir(directory_name)
            print(f"Directory '{directory_name}' created successfully.")
        except PermissionError:
            print(f"Permission denied: Unable to create '{directory_name}'.")
        except Exception as e:
            print(f"An error occurred: {e}")

    return directory_name


def generate_file_path(directory: str, base_name: str, extension: str) -> str:
    """Generates a unique file path in the specified directory."""
    num = 0
    while True:
        file_name = f"{base_name}_{num}.{extension}"
        file_path = os.path.join(directory, file_name)
        if not os.path.exists(file_path):
            return file_path  # Return the unique file path
        num += 1


def directory_path(subject: str, lang: str) -> str:
    # Determine the directory path for the exercise
    directory_name = f"{subject}_{lang.lower()}"
    full_directory_path = os.path.join(os.getcwd(), directory_name)

    # Create the directory if it does not exist
    create_directory(full_directory_path)
    return full_directory_path
