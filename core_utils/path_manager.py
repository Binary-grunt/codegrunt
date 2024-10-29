from core_utils.directory_manager import DirectoryManager
import os


class PathManager:
    current_exercise_file_path = None

    def __init__(self):
        self.directory_manager = DirectoryManager()

    @staticmethod
    def set_current_exercise_path(path: str):
        # Set the path for the current exercise file.
        PathManager.current_exercise_file_path = path

    @staticmethod
    def get_current_exercise_path() -> str:
        # Get the path for the current exercise file.
        return PathManager.current_exercise_file_path

    @staticmethod
    def get_evaluated_file_path(file_path: str) -> str:
        # Get the path in the same directory as the file being evaluated
        directory = os.path.dirname(file_path)
        return os.path.join(directory, 'evaluated_exercises.txt')

    @staticmethod
    def generate_file_path(directory: str, base_name: str, extension: str) -> str:
        # Generates a unique file path in the specified directory
        num = 0
        while True:
            file_name = f"{base_name}_{num}.{extension}"
            file_path = os.path.join(directory, file_name)
            if not os.path.exists(file_path):
                return file_path  # Return the unique file path
            num += 1

    def get_directory_path(self, subject: str, lang: str) -> str:
        # Use DirectoryManager to get or create directory path
        return self.directory_manager.directory_path(subject, lang)
