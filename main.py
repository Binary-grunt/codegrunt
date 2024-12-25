from database import initialization_db
from database.sqlite_config import SessionLocal
import typer
from api import OpenAIService
from core.interface_cli import ApplicationInterface, PreferenceCli
from core.session_manager import SessionManager
from core.managers import UserManager, ExerciseManager


def main():
    initialization_db()
    db = SessionLocal()
    openai_service = OpenAIService()
    exercise_manager = ExerciseManager(openai_service)
    session_manager = SessionManager(db, exercise_manager)

    # Initialize components
    user_manager = UserManager(session_manager)
    preference_manager = PreferenceCli()
    app_interface = ApplicationInterface(session_manager, user_manager, preference_manager)

    # Run the application
    app_interface.run()


if __name__ == "__main__":
    typer.run(main)
