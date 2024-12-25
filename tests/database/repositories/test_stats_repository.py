import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base, Stats, Sessions
from database.repositories.stats_repository import StatsRepository

# Fixture for in-memory SQLite database


@pytest.fixture(scope="function")
def db_session():
    """
    Creates a new SQLAlchemy session with an in-memory SQLite database for each test.
    """
    # Create an in-memory SQLite database
    engine = create_engine("sqlite:///:memory:", echo=False)  # Set echo=True for debugging queries
    Base.metadata.create_all(bind=engine)  # Create tables

    # Create a session factory
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    try:
        yield db  # Provide the session to the test
    finally:
        db.close()

# Fixture for StatsRepository


@pytest.fixture(scope="function")
def stats_repository(db_session):
    """
    Creates a StatsRepository instance using the in-memory SQLite database.
    """
    return StatsRepository(db=db_session)

# Tests


def test_calculate_user_stats_empty(stats_repository, db_session):
    """
    Test calculate_user_stats returns default values when no sessions exist.
    """
    stats = stats_repository.calculate_user_stats(user_id=1)
    assert stats == {"total_sessions": 0, "total_exercises": 0, "average_score": 0.0}


def test_calculate_user_stats_with_sessions(stats_repository, db_session):
    """
    Test calculate_user_stats calculates stats correctly based on sessions.
    """
    # Add sessions for a user
    session1 = Sessions(user_id=1, score=50, exercises_completed=5)
    session2 = Sessions(user_id=1, score=80, exercises_completed=8)
    db_session.add_all([session1, session2])
    db_session.commit()

    stats = stats_repository.calculate_user_stats(user_id=1)
    assert stats["total_sessions"] == 2
    assert stats["total_exercises"] == 13
    assert stats["average_score"] == 65.0  # (50 + 80) / 2


def test_create_or_update_stats_new(stats_repository, db_session):
    """
    Test create_or_update_stats creates a new stats entry if none exists.
    """
    # Add sessions for a user
    session1 = Sessions(user_id=1, score=90, exercises_completed=9)
    db_session.add(session1)
    db_session.commit()

    stats = stats_repository.create_or_update_stats(user_id=1)

    assert stats is not None
    assert stats.user_id == 1
    assert stats.total_sessions == 1
    assert stats.total_exercises == 9
    assert stats.average_score == 90.0

    # FIX: Fix that test
# def test_create_or_update_stats_update_existing(stats_repository, db_session):
#     """
#     Test create_or_update_stats updates existing stats correctly.
#     """
#     # Create initial stats
#     initial_stats = Stats(user_id=1, total_sessions=1, total_exercises=10, average_score=85.0)
#     db_session.add(initial_stats)
#     db_session.commit()
#
#     # Add more sessions for the user
#     session1 = Sessions(user_id=1, score=75, exercises_completed=5)
#     session2 = Sessions(user_id=1, score=95, exercises_completed=7)
#     db_session.add_all([session1, session2])
#     db_session.commit()
#
#     updated_stats = stats_repository.create_or_update_stats(user_id=1)
#
#     assert updated_stats.total_sessions == 3
#     assert updated_stats.total_exercises == 22  # 10 + 5 + 7
#     assert round(updated_stats.average_score, 2) == 85.0  # Weighted average recalculated


def test_get_stats_by_user(stats_repository, db_session):
    """
    Test get_stats_by_user retrieves the correct stats for a user.
    """
    # Create a stats entry
    stats_entry = Stats(user_id=1, total_sessions=2, total_exercises=15, average_score=78.0)
    db_session.add(stats_entry)
    db_session.commit()

    stats = stats_repository.get_stats_by_user(user_id=1)
    assert stats is not None
    assert stats.user_id == 1
    assert stats.total_sessions == 2
    assert stats.total_exercises == 15
    assert stats.average_score == 78.0


def test_get_stats_by_user_not_found(stats_repository):
    """
    Test get_stats_by_user returns None if the user has no stats.
    """
    stats = stats_repository.get_stats_by_user(user_id=999)
    assert stats is None


def test_reset_stats(stats_repository, db_session):
    """
    Test reset_stats deletes the stats entry for a user.
    """
    # Create a stats entry
    stats_entry = Stats(user_id=1, total_sessions=3, total_exercises=20, average_score=82.0)
    db_session.add(stats_entry)
    db_session.commit()

    result = stats_repository.reset_stats(user_id=1)
    assert result is True
    assert db_session.query(Stats).filter(Stats.user_id == 1).count() == 0


def test_reset_stats_not_found(stats_repository):
    """
    Test reset_stats returns False if no stats exist for the user.
    """
    result = stats_repository.reset_stats(user_id=999)
    assert result is False
