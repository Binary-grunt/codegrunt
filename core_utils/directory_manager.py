import os


class DirectoryManager:
    @staticmethod
    def create_directory(directory_name: str) -> str:
        # Create a directory if it does not exist and return its name.
        if not os.path.exists(directory_name):
            try:
                os.mkdir(directory_name)
                print(f"Directory '{directory_name}' created successfully.")
            except PermissionError:
                print(f"Permission denied: Unable to create '{
                      directory_name}'.")
            except Exception as e:
                print(f"An error occurred: {e}")
        return directory_name

    @staticmethod
    def directory_path(subject: str, lang: str) -> str:
        # Generate the directory path based on subject and language, create it if needed
        directory_name = f"{subject}_{lang.lower()}"
        full_directory_path = os.path.join(os.getcwd(), directory_name)
        DirectoryManager.create_directory(full_directory_path)
        return full_directory_path
