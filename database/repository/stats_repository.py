from sqlalchemy.orm import Session
from database.models import Stats


class StatsRepository:
    def __init__(self, db: Session):
        """
        Repository for Stats entity.

        Args:
            db (Session): SQLAlchemy session object.
        """
        self.db = db

    def create_or_update_stats(self, user_id: int, total_sessions: int, total_exercises: int, average_score: float) -> Stats:
        """
        Create or update the stats for a given user.

        Args:
            user_id (int): ID of the user.
            total_sessions (int): Total number of sessions.
            total_exercises (int): Total number of exercises completed.
            average_score (float): Average score per session.

        Returns:
            Stats: The updated or newly created stats object.
        """
        stats = self.get_stats_by_user(user_id)
        if stats:
            stats.average_score = (
                (stats.average_score * stats.total_sessions + average_score * total_sessions) / (stats.total_sessions + total_sessions)
            )
            stats.total_sessions += total_sessions
            stats.total_exercises += total_exercises
        else:
            stats = Stats(
                user_id=user_id,
                total_sessions=total_sessions,
                total_exercises=total_exercises,
                average_score=average_score
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
