from infrastructure.database.models import User
from sqlalchemy.orm import Session


class UserRepository:
    def __init__(self, db: Session):
        """
        Repository for User entity.

        Args:
            db (Session): SQLAlchemy session object.
        """
        self.db = db

    def add_user(self) -> User:
        """
        Add a new user to the database.

        Returns:
            User: The newly created user.
        """
        new_user = User()
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def get_user_by_id(self, user_id: int) -> User:
        """
        Retrieve a user by ID.

        Args:
            user_id (int): The ID of the user.

        Returns:
            User: The user object, or None if not found.
        """
        return self.db.query(User).filter(User.id == user_id).first()

    def list_all_users(self) -> list[User]:
        """
        List all users in the database.

        Returns:
            list[User]: A list of all users.
        """
        return self.db.query(User).all()
