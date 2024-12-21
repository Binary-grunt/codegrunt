from sqlalchemy.orm import Session
from infrastructure.database.models import Sessions as SessionsModel


class SessionsRepository:
    def __init__(self, db: Session):
        """
        Repository for Session entity.

        Args:
            db (Session): SQLAlchemy session object.
        """
        self.db = db

    def create_session(self, user_id: int, score: int, exercises_completed: int, successful_exercises: int) -> SessionsModel:
        """
        Create a new session for a user.

        Args:
            user_id (int): ID of the user.
            score (int): Total score for the session.
            exercises_completed (int): Number of exercises completed.
            successful_exercises (int): Number of successful exercises.

        Returns:
            SessionModel: The newly created session.
        """
        new_session = SessionsModel(
            user_id=user_id,
            score=score,
            exercises_completed=exercises_completed,
            successful_exercises=successful_exercises
        )
        self.db.add(new_session)
        self.db.commit()
        self.db.refresh(new_session)
        return new_session

    def get_sessions_by_user(self, user_id: int):
        """
        Retrieve all sessions for a given user.

        Args:
            user_id (int): ID of the user.

        Returns:
            list[SessionModel]: List of sessions for the user.
        """
        return self.db.query(SessionsModel).filter(SessionsModel.user_id == user_id).all()

    def get_session_by_id(self, session_id: int) -> SessionsModel:
        """
        Retrieve a session by its ID.

        Args:
            session_id (int): The ID of the session.

        Returns:
            SessionModel: The session object, or None if not found.
        """
        return self.db.query(SessionsModel).filter(SessionsModel.id == session_id).first()

    def delete_session(self, session_id: int) -> bool:
        """
        Delete a session by its ID.

        Args:
            session_id (int): The ID of the session.

        Returns:
            bool: True if the session was deleted, False otherwise.
        """
        session = self.get_session_by_id(session_id)
        if session:
            self.db.delete(session)
            self.db.commit()
            return True
        return False
