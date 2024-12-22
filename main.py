from api import OpenAIService
from core.exercise_manager import ExerciseManager
# from infrastructure.database import initialization_db
# from infrastructure.database.sqlite_config import SessionLocal
# from infrastructure.repository import SessionsRepository, StatsRepository

# TODO: Refactoriying the code, make a class for DB SQLITE


def main():
    try:
        # Get the singleton instance of OpenAIService
        openai_service = OpenAIService()

        # Initialize ExerciseManager with the singleton OpenAIService
        exercise_manager = ExerciseManager(openai_service)

        # Test the generate_exercise method in ExerciseManager
        print(exercise_manager.generate_exercise("OOP", "typescript", "beginner"))

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

    except ValueError as e:
        print(e)


if __name__ == "__main__":
    print("Starting Code Grunt...")
    main()
    while True:
        pass  # Keep the process alive (replace this with meaningful logic if needed)
