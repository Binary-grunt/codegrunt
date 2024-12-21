import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base, User
from database.repository import UserRepository

# Fixture for in-memory SQLite database


@pytest.fixture(scope="function")
def db_session():
    """
    Creates a new SQLAlchemy session with an in-memory SQLite database for each test.
    """
    # Create an in-memory SQLite database
    engine = create_engine("sqlite:///:memory:", echo=True)
    Base.metadata.create_all(bind=engine)  # Create tables

    # Create a session factory
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    try:
        yield db  # Provide the session to the test
    finally:
        db.close()

# Fixture for UserRepository


@pytest.fixture(scope="function")
def user_repository(db_session):
    """
    Creates a UserRepository instance using the in-memory SQLite database.
    """
    return UserRepository(db=db_session)

# Test cases for UserRepository


def test_add_user(user_repository, db_session):
    """
    Test the add_user method.
    """
    # Add a user
    new_user = user_repository.add_user()

    # Verify the user was added
    assert new_user.id is not None
    assert db_session.query(User).count() == 1
    assert db_session.query(User).first().id == new_user.id


def test_get_user_by_id(user_repository):
    """
    Test the get_user_by_id method.
    """
    # Add a user
    new_user = user_repository.add_user()

    # Retrieve the user by ID
    retrieved_user = user_repository.get_user_by_id(new_user.id)

    # Verify the retrieved user matches the added user
    assert retrieved_user is not None
    assert retrieved_user.id == new_user.id


def test_get_user_by_id_not_found(user_repository):
    """
    Test get_user_by_id returns None if the user does not exist.
    """
    # Try to retrieve a non-existent user
    retrieved_user = user_repository.get_user_by_id(999)

    # Verify no user is found
    assert retrieved_user is None


def test_list_all_users(user_repository):
    """
    Test the list_all_users method.
    """
    # Add multiple users
    user1 = user_repository.add_user()
    user2 = user_repository.add_user()

    # Retrieve all users
    users = user_repository.list_all_users()

    # Verify the list contains all added users
    assert len(users) == 2
    assert user1.id in [user.id for user in users]
    assert user2.id in [user.id for user in users]


def test_list_all_users_empty(user_repository):
    """
    Test list_all_users returns an empty list when there are no users.
    """
    # Retrieve all users from an empty database
    users = user_repository.list_all_users()

    # Verify the list is empty
    assert len(users) == 0
