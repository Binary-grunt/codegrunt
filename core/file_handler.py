import os
from config.constants import FILE_EXTENSIONS


class FileHandler:
    """
    Handles file and directory operations.
    """

    def __init__(self, base_dir: str):
        """
        Initialize the FileHandler with a base directory.

        Args:
            base_dir (str): The base directory for file operations.
        """
        self.base_dir = base_dir
        self._ensure_directory_exists(base_dir)

    @staticmethod
    def get_extension(language: str) -> str:
        """
        Retrieves the appropriate file extension for the given language.

        Args:
            language (str): Programming language.

        Returns:
            str: The file extension for the language.

        Raises:
            ValueError: If the language is not supported.
        """
        extension = FILE_EXTENSIONS.get(language.lower())
        if not extension:
            raise ValueError(f"Unsupported language: {language}")
        return extension

    def _ensure_directory_exists(self, path: str) -> None:
        """
        Ensures that the specified directory exists; creates it if necessary.

        Args:
            path (str): The directory path.
        """
        if not os.path.exists(path):
            os.makedirs(path)

    @classmethod
    def initialize_session_path(cls, root_dir: str, language: str, subject: str, level: str, session_id: int) -> str:
        """
        Initializes and returns the session-specific path for storing exercises.

        Args:
            root_dir (str): Root directory for exercises.
            language (str): Programming language.
            subject (str): Subject/topic of the exercises.
            level (str): Difficulty level.
            session_id (int): Session identifier.

        Returns:
            str: The initialized session path.
        """
        session_folder_name = f"{level}_{subject}_{session_id}"
        session_path = os.path.join(root_dir, language, session_folder_name)
        os.makedirs(session_path, exist_ok=True)
        return session_path

    def get_next_iteration(self, subject: str) -> int:
        """
        Determines the next available iteration number for files in the session directory.

        Args:
            subject (str): The subject/topic of the exercises.

        Returns:
            int: The next available iteration number.
        """
        existing_files = os.listdir(self.base_dir)
        iterations = [
            int(file.split("_")[-1].split(".")[0])
            for file in existing_files if file.startswith(subject)
        ]
        return max(iterations, default=0) + 1

    def save_to_file(self, file_name: str, content: str) -> str:
        """
        Saves content to a file.

        Args:
            file_name (str): Name of the file.
            content (str): Content to save in the file.

        Returns:
            str: Full path of the saved file.
        """
        file_path = os.path.join(self.base_dir, file_name)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content.strip())
        return file_path
