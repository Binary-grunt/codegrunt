from core.managers.exercise_manager import ExerciseManager
from .file_handler import FileHandler
from common.utils.validator import Validator


class ExerciseGenerator:
    """
    Manages the creation of folders, files, and exercises using OpenAI API.
    """

    DEFAULT_ROOT_DIR = "exercises"

    def __init__(self, language: str, subject: str, level: str, session_id: int, exercise_manager: ExerciseManager):
        """
        Initialize the generator with language, subject, level, and session ID.

        Args:
            language (str): Programming language.
            subject (str): Subject/topic of the exercises.
            level (str): Difficulty level (e.g., beginner, intermediate, advanced, expert).
            session_id (int): Session identifier.
            exercise_manager (ExerciseManager): An instance of ExerciseManager to generate exercises.
        """
        self.language = Validator.validate_input(language, "language")
        self.subject = Validator.validate_input(subject, "subject")
        self.level = Validator.validate_input(level, "level")
        self.session_id = session_id
        self.exercise_manager = exercise_manager

        # Initialize FileHandler with session-specific base path
        base_path = FileHandler.initialize_session_path(
            self.DEFAULT_ROOT_DIR, self.language, self.subject, self.level, self.session_id
        )
        self.file_handler = FileHandler(base_path)

    def generate_and_save_exercise(self) -> str:
        """
        Generates an exercise using OpenAI and saves it to a file.

        Returns:
            str: Path of the saved exercise file.
        """
        try:
            # Generate exercise content
            exercise_content = self.exercise_manager.generate_exercise(
                subject=self.subject,
                language=self.language,
                level=self.level
            )

            # Get file extension and iteration
            file_extension = self.file_handler.get_extension(self.language)
            iteration = self.file_handler.get_next_iteration(self.subject)

            # Construct file name and save the file
            file_name = f"{self.subject}_{iteration}.{file_extension}"
            return self.file_handler.save_to_file(file_name, exercise_content)

        except Exception as e:
            raise RuntimeError(f"Failed to generate and save exercise: {e}") from e
