from api import OpenAIService
from core import ExerciseManager, ExerciseGenerator
import typer
from rich import print
# from infrastructure.database import initialization_db
# from infrastructure.database.sqlite_config import SessionLocal
# from infrastructure.repository import SessionsRepository, StatsRepository

# TODO: Refactoriying the code, make a class for DB SQLITE


def main():
    try:
        # Initialize the OpenAIService and ExerciseManager
        openai_service = OpenAIService()
        exercise_manager = ExerciseManager(openai_service)
        language = "python"
        subject = "OOP"
        level = "advanced"

        generator = ExerciseGenerator(language, subject, level, exercise_manager)
        while True:
            command = input("Enter command (submit/exit): ").strip().lower()

            if command == "submit":
                # Generate and save the exercise
                file_path = generator.generate_and_save_exercise()
                print(f"Exercise saved at: {file_path}")
            elif command == "exit":
                print("Exiting...")
                break
            else:
                print("Invalid command. Use 'submit' or 'exit'.")
    except ValueError as e:
        print(f"Error: {e}")

        # # Initialized the database
        # initialization_db()
        # with SessionLocal() as db:
        #     session_repo = SessionsRepository(db)
        #     stats_repo = StatsRepository(db)
        #
        #     # Create a new session
        #     session = session_repo.create_session(user_id=1, score=90, exercises_completed=5, successful_exercises=4)
        #     print(f"Created session: {session.id}")
        #
        #     # Update stats
        #     stats = stats_repo.create_or_update_stats(user_id=1, total_sessions=1, total_exercises=5, average_score=90.0)
        #     print(f"Updated stats: {stats.average_score}")
        #
        #     # Retrieve sessions
        #     sessions = session_repo.get_sessions_by_user(user_id=1)
        #     print(f"User 1 has {len(sessions)} sessions.")

        print("Starting Code Grunt...")
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    typer.run(main)
    while True:
        pass  # Keep the process alive (replace this with meaningful logic if needed)
