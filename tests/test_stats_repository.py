import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from infrastructure.database.models import Base, Stats
from infrastructure.repository import StatsRepository

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

# Fixture for StatsRepository


@pytest.fixture(scope="function")
def stats_repository(db_session):
    """
    Creates a StatsRepository instance using the in-memory SQLite database.
    """
    return StatsRepository(db=db_session)

# Test cases for StatsRepository


def test_create_or_update_stats_new(stats_repository, db_session):
    """
    Test the create_or_update_stats method for creating new stats.
    """
    # Create stats for a user
    stats = stats_repository.create_or_update_stats(
        user_id=1,
        total_sessions=1,
        total_exercises=10,
        average_score=85.0
    )

    # Verify the stats were created
    assert stats is not None
    assert stats.user_id == 1
    assert stats.total_sessions == 1
    assert stats.total_exercises == 10
    assert stats.average_score == 85.0
    assert db_session.query(Stats).count() == 1


def test_create_or_update_stats_update(stats_repository):
    """
    Test the create_or_update_stats method for updating existing stats.
    """
    # Create initial stats
    stats_repository.create_or_update_stats(
        user_id=1,
        total_sessions=1,
        total_exercises=10,
        average_score=85.0
    )

    # Update stats for the same user
    updated_stats = stats_repository.create_or_update_stats(
        user_id=1,
        total_sessions=2,
        total_exercises=20,
        average_score=90.0
    )

    # Verify the stats were updated correctly
    assert updated_stats.total_sessions == 3
    assert updated_stats.total_exercises == 30
    assert round(updated_stats.average_score, 2) == 88.33  # Weighted average


def test_get_stats_by_user(stats_repository):
    """
    Test the get_stats_by_user method.
    """
    # Create stats
    stats_repository.create_or_update_stats(
        user_id=1,
        total_sessions=1,
        total_exercises=10,
        average_score=85.0
    )

    # Retrieve stats for the user
    stats = stats_repository.get_stats_by_user(user_id=1)

    # Verify the retrieved stats
    assert stats is not None
    assert stats.user_id == 1
    assert stats.total_sessions == 1
    assert stats.total_exercises == 10
    assert stats.average_score == 85.0


def test_get_stats_by_user_not_found(stats_repository):
    """
    Test get_stats_by_user returns None if the stats do not exist.
    """
    # Try to retrieve stats for a non-existent user
    stats = stats_repository.get_stats_by_user(user_id=999)

    # Verify no stats are found
    assert stats is None


def test_reset_stats(stats_repository, db_session):
    """
    Test the reset_stats method.
    """
    # Create stats
    stats_repository.create_or_update_stats(
        user_id=1,
        total_sessions=1,
        total_exercises=10,
        average_score=85.0
    )

    # Reset stats for the user
    result = stats_repository.reset_stats(user_id=1)

    # Verify the stats were deleted
    assert result is True
    assert db_session.query(Stats).filter(Stats.user_id == 1).count() == 0


def test_reset_stats_not_found(stats_repository):
    """
    Test reset_stats returns False if the stats do not exist.
    """
    # Try to reset stats for a non-existent user
    result = stats_repository.reset_stats(user_id=999)

    # Verify no stats were deleted
    assert result is False
