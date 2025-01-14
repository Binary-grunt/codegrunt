from sqlalchemy.orm import Session
from database.models import Sessions, Stats


class StatsRepository:
    def __init__(self, db: Session):
        """
        Repository for Stats entity.

        Args:
            db (Session): SQLAlchemy session object.
        """
        self.db = db

    def calculate_user_stats(self, user_id: int) -> dict:
        """
        Calculates the aggregate stats for a user based on their sessions.

        Args:
            user_id (int): The ID of the user.

        Returns:
            dict: A dictionary containing total_sessions, total_exercises, and average_score.
        """
        # Fetch all sessions for the user
        sessions = self.db.query(Sessions).filter(Sessions.user_id == user_id).all()
        valid_sessions = [session for session in sessions if session.exercises_completed >= 10]

        if not valid_sessions:
            return {"total_sessions": 0, "total_exercises": 0, "average_score": 0.0}

        # Calculate statistics based on validated sessions
        total_sessions = len(valid_sessions)
        total_exercises = sum(session.exercises_completed for session in valid_sessions)
        average_score = sum(session.score for session in valid_sessions) / total_sessions

        return {
            "total_sessions": total_sessions,
            "total_exercises": total_exercises,
            "average_score": round(average_score, 2),  # Round to 2 decimal places for clarity
        }

    def create_or_update_stats(self, user_id: int) -> Stats:
        """
        Create or update the stats for a given user based on the most recent sessions.

        Args:
            user_id (int): ID of the user.

        Returns:
            Stats: The updated or newly created stats object.
        """
        # Récupérer les statistiques existantes
        stats = self.get_stats_by_user(user_id)

        # Calculer les nouvelles statistiques
        stats_data = self.calculate_user_stats(user_id)

        if stats:
            # Remplacer les statistiques par les données recalculées
            stats.total_sessions = stats_data["total_sessions"]
            stats.total_exercises = stats_data["total_exercises"]
            stats.average_score = stats_data["average_score"]
        else:
            # Créer une nouvelle entrée si aucune statistique n'existe
            stats = Stats(
                user_id=user_id,
                total_sessions=stats_data["total_sessions"],
                total_exercises=stats_data["total_exercises"],
                average_score=stats_data["average_score"],
            )
            self.db.add(stats)

        self.db.commit()
        self.db.refresh(stats)
        return stats

    def get_stats_by_user(self, user_id: int) -> Stats:
        """
        Retrieve the stats for a given user.

        Args:
            user_id (int): ID of the user.

        Returns:
            Stats: The stats object, or None if not found.
        """
        return self.db.query(Stats).filter(Stats.user_id == user_id).first()

    def reset_stats(self, user_id: int) -> bool:
        """
        Reset the stats for a user (delete stats entry).

        Args:
            user_id (int): ID of the user.

        Returns:
            bool: True if the stats were deleted, False otherwise.
        """
        stats = self.get_stats_by_user(user_id)
        if stats:
            self.db.delete(stats)
            self.db.commit()
            return True
        return False
