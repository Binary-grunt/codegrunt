import typer
from database import initialization_db
from database.sqlite_config import SessionLocal
from api import OpenAIService
from core.cli import PreferenceCli
from core.session_manager import SessionManager
from core.managers import UserManager, ExerciseManager
from core.cli_controller import CliController


def main() -> None:
    """
    Entry point for the CodeGrunt CLI application.

    This function initializes the database, sets up necessary managers,
    and then launches the main CLI controller. It uses Typer for command-line
    argument parsing and execution.
    """
    initialization_db()
    db = SessionLocal()

    openai_service = OpenAIService()
    exercise_manager = ExerciseManager(openai_service)
    session_manager = SessionManager(db, exercise_manager)
    user_manager = UserManager(session_manager)
    preference_manager = PreferenceCli()

    app_interface = CliController(session_manager, user_manager, preference_manager)

    app_interface.run()


if __name__ == "__main__":
    typer.run(main)
