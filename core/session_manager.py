from sqlalchemy.orm import Session
from database.repositories.sessions_repository import SessionsRepository
from database.repositories.stats_repository import StatsRepository
from database.repositories.user_repository import UserRepository
from core.managers import ExerciseManager
from core.exercise_generator import ExerciseGenerator
import os


class SessionManager:
    """
    Manages user sessions, exercises, and scoring logic with OpenAI integration.
    """

    MAX_EXERCISES_PER_SESSION = 10

    def __init__(self, db: Session, exercise_manager: ExerciseManager):
        """
        Initialize the SessionManager with necessary dependencies.

        Args:
            db (Session): SQLAlchemy database session.
            exercise_manager (ExerciseManager): Instance of ExerciseManager to manage exercises.
        """
        self.db = db
        self.sessions_repository = SessionsRepository(db)
        self.stats_repository = StatsRepository(db)
        self.user_repository = UserRepository(db)
        self.exercise_manager = exercise_manager
        self.current_session = None
        self.last_generated_file = None

    def start_new_session(self, user_id: int) -> None:
        """
        Starts a new session for the user if no session exists or the current session is full.

        Args:
            user_id (int): The ID of the user.
        """
        # Check if an active session exists and has space for more exercises
        if (
            self.current_session and
            self.current_session.user_id == user_id and
            self.current_session.exercises_completed < self.MAX_EXERCISES_PER_SESSION
        ):
            return  # Keep using the current session

        # Otherwise, create a new session
        self.current_session = self.sessions_repository.create_session(
            user_id=user_id,
            score=0,
            exercises_completed=0,
            successful_exercises=0,
        )

    def create_new_exercise(self, user_id: int, language: str, subject: str, level: str) -> str:
        """
        Generates an exercise using ExerciseGenerator and saves it to a file.

        Args:
            user_id (int): The ID of the user generating the exercise.
            language (str): The programming language.
            subject (str): The subject of the exercise.
            level (str): The difficulty level.

        Returns:
            str: The path of the generated exercise file.
        """
        # Ensure a valid session exists
        self.start_new_session(user_id)

        # Generate the exercise using the current session ID for the folder structure
        generator = ExerciseGenerator(
            language=language,
            subject=subject,
            level=level,
            session_id=self.current_session.id,
            exercise_manager=self.exercise_manager
        )
        file_path = generator.generate_and_save_exercise()
        self.last_generated_file = file_path
        return file_path

    def submit_exercise(self, user_id: int, file_path: str = None) -> str:
        """
        Submits an exercise file for analysis, updates the session, and calculates the score.

        Args:
            user_id (int): The ID of the user submitting the exercise.
            file_path (str): Path to the exercise file.

        Returns:
            str: Feedback message about the submission.
        """
        file_path = file_path or self.last_generated_file
        if not file_path:
            raise ValueError("No exercise file has been generated yet.")

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file '{file_path}' does not exist.")

        with open(file_path, "r", encoding="utf-8") as file:
            file_content = file.read()

        # Analyze the file content using ExerciseManager
        analysis_result = self.exercise_manager.analyze_code(file_content)

        # Update the current session based on the analysis result
        if self.current_session.exercises_completed >= self.MAX_EXERCISES_PER_SESSION:
            self.start_new_session(user_id)

        feedback = self._update_score_session(analysis_result)
        self.db.commit()

        # Update user stats
        self.stats_repository.create_or_update_stats(user_id)

        return feedback

    def _is_session_complete(self) -> bool:
        """
        Check if the current session is complete.
        """
        return self.current_session.exercises_completed >= self.MAX_EXERCISES_PER_SESSION

    def _update_score_session(self, analysis_result: str) -> str:
        """
        Processes the result of the submission and updates the session.

        Args:
            analysis_result (str): Result of the exercise analysis.

        Returns:
            str: Feedback message based on the analysis result.
        """
        if analysis_result == "Result: True":
            self.current_session.score += 10
            self.current_session.successful_exercises += 1
            feedback = "Exercise was correct! +10 points."
        else:
            feedback = "Exercise was incorrect. No points awarded."

        self.current_session.exercises_completed += 1
        if self._is_session_complete():
            feedback += (
                f"\nSession Complete! Total Exercises: {self.current_session.exercises_completed}, "
                f"Successful: {self.current_session.successful_exercises}, "
                f"Unsuccessful: {self.current_session.exercises_completed - self.current_session.successful_exercises}."
            )
            # Optionally, you could also reset the session here
            self.current_session = None

        return feedback
