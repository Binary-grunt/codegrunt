import os
from datetime import datetime
from .exercise_manager import ExerciseManager
from .file_handler import FileHandler
from common.utils.validator import Validator


class ExerciseGenerator:
    """
    Manages the creation of folders, files, and exercises using OpenAI API.
    """

    DEFAULT_ROOT_DIR = "exercises"

    def __init__(self, language: str, subject: str, level: str, exercise_manager: ExerciseManager):
        """
        Initialize the generator with language, subject, and level.

        Args:
            language (str): Programming language.
            subject (str): Subject/topic of the exercises.
            level (str): Difficulty level (e.g., beginner, intermediate, advanced, expert).
            exercise_manager (ExerciseManager): An instance of ExerciseManager to generate exercises.
        """
        self.language = Validator.validate_input(language, "language")
        self.subject = Validator.validate_input(subject, "subject")
        self.level = Validator.validate_input(level, "level")
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        self.iteration = 1  # Start with the first exercise
        self.exercise_manager = exercise_manager
        self.file_handler = None  # Initialized dynamically when needed

    def get_base_path(self) -> str:
        """
        Generates the base path for saving exercises.

        Returns:
            str: The base path.
        """
        return os.path.join(
            self.DEFAULT_ROOT_DIR,
            self.language,
            f"{self.subject}_{self.level}_{self.timestamp}"
        )

    def generate_and_save_exercise(self) -> str:
        """
        Generates an exercise using OpenAI and saves it to a file.

        Returns:
            str: Path of the saved exercise file.

        Raises:
            RuntimeError: If the exercise content could not be generated or saved.
        """
        try:
            self._initialize_file_handler()
            exercise_content = self._generate_exercise_content()
            file_name = self._construct_file_name()
            file_path = self.file_handler.save_to_file(file_name, exercise_content)

            self.iteration += 1

            return file_path

        except Exception as e:
            raise RuntimeError(f"Failed to generate and save exercise: {e}") from e

    def _generate_exercise_content(self) -> str:
        """
        Generates the content of the exercise using the ExerciseManager.

        Returns:
            str: The generated exercise content.

        Raises:
            RuntimeError: If the content could not be generated.
        """
        try:
            return self.exercise_manager.generate_exercise(
                subject=self.subject,
                language=self.language,
                level=self.level
            )
        except Exception as e:
            raise RuntimeError(f"Failed to generate exercise content: {e}") from e

    def _construct_file_name(self) -> str:
        """
        Constructs the file name for the exercise file.

        Returns:
            str: The constructed file name.
        """
        base_subject = self.subject.split("_")[-1]  # Extract main subject if necessary
        return f"{base_subject}_{self.iteration}.py"

    def _initialize_file_handler(self):
        """
        Initializes the file handler if it has not been created yet.
        """
        if not self.file_handler:
            base_path = self.get_base_path()
            self.file_handler = FileHandler(base_path)
