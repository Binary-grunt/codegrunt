import os


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

    def _ensure_directory_exists(self, path: str) -> None:
        """
        Ensures that the specified directory exists; creates it if necessary.

        Args:
            path (str): The directory path.
        """
        if not os.path.exists(path):
            os.makedirs(path)

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
