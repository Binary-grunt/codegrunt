import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base, Sessions
from database.repositories import SessionsRepository

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

# Fixture for SessionsRepository


@pytest.fixture(scope="function")
def sessions_repository(db_session):
    """
    Creates a SessionsRepository instance using the in-memory SQLite database.
    """
    return SessionsRepository(db=db_session)

# Test cases for SessionsRepository


def test_create_session(sessions_repository, db_session):
    """
    Test the create_session method.
    """
    # Create a new session
    new_session = sessions_repository.create_session(
        user_id=1,
        score=95,
        exercises_completed=10,
        successful_exercises=8
    )

    # Verify the session was created
    assert new_session is not None
    assert new_session.id is not None
    assert new_session.user_id == 1
    assert new_session.score == 95
    assert new_session.exercises_completed == 10
    assert new_session.successful_exercises == 8
    assert db_session.query(Sessions).count() == 1


def test_get_sessions_by_user(sessions_repository, db_session):
    """
    Test the get_sessions_by_user method.
    """
    # Create sessions for user 1
    sessions_repository.create_session(user_id=1, score=80, exercises_completed=5, successful_exercises=4)
    sessions_repository.create_session(user_id=1, score=90, exercises_completed=6, successful_exercises=5)

    # Create a session for user 2
    sessions_repository.create_session(user_id=2, score=70, exercises_completed=4, successful_exercises=3)

    # Retrieve sessions for user 1
    user_sessions = sessions_repository.get_sessions_by_user(user_id=1)

    # Verify the correct sessions are retrieved
    assert len(user_sessions) == 2
    for session in user_sessions:
        assert session.user_id == 1


def test_get_session_by_id(sessions_repository):
    """
    Test the get_session_by_id method.
    """
    # Create a new session
    new_session = sessions_repository.create_session(
        user_id=1,
        score=85,
        exercises_completed=7,
        successful_exercises=6
    )

    # Retrieve the session by ID
    retrieved_session = sessions_repository.get_session_by_id(session_id=new_session.id)

    # Verify the session matches the created one
    assert retrieved_session is not None
    assert retrieved_session.id == new_session.id
    assert retrieved_session.user_id == new_session.user_id


def test_get_session_by_id_not_found(sessions_repository):
    """
    Test get_session_by_id returns None if the session does not exist.
    """
    # Try to retrieve a non-existent session
    session = sessions_repository.get_session_by_id(session_id=999)

    # Verify no session is found
    assert session is None


def test_delete_session(sessions_repository, db_session):
    """
    Test the delete_session method.
    """
    # Create a new session
    new_session = sessions_repository.create_session(
        user_id=1,
        score=75,
        exercises_completed=8,
        successful_exercises=7
    )

    # Delete the session
    result = sessions_repository.delete_session(session_id=new_session.id)

    # Verify the session was deleted
    assert result is True
    assert db_session.query(Sessions).filter(Sessions.id == new_session.id).count() == 0


def test_delete_session_not_found(sessions_repository):
    """
    Test delete_session returns False if the session does not exist.
    """
    # Try to delete a non-existent session
    result = sessions_repository.delete_session(session_id=999)

    # Verify no session was deleted
    assert result is False
