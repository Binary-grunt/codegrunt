import pytest
from unittest.mock import MagicMock
from core.managers import ExerciseManager
from core.session_manager import SessionManager


@pytest.fixture
def mock_db():
    """
    Mock the database session.
    """
    return MagicMock()


@pytest.fixture
def mock_exercise_manager():
    """
    Mock the ExerciseManager.
    """
    manager = MagicMock(spec=ExerciseManager)
    manager.analyze_code.return_value = "Result: True"
    return manager


@pytest.fixture
def session_manager(mock_db, mock_exercise_manager):
    """
    Provide a SessionManager instance with mocked dependencies.
    """
    return SessionManager(mock_db, mock_exercise_manager)


def test_start_new_session_creates_session(session_manager):
    """
    Test starting a new session when no current session exists.
    """
    mock_user_id = 1
    session_manager.sessions_repository.create_session = MagicMock(return_value=MagicMock(id=1, user_id=mock_user_id))

    session_manager.start_new_session(mock_user_id)

    session_manager.sessions_repository.create_session.assert_called_once_with(
        user_id=mock_user_id, score=0, exercises_completed=0, successful_exercises=0
    )
    assert session_manager.current_session is not None
    assert session_manager.current_session.user_id == mock_user_id


def test_submit_exercise_updates_session_and_stats(session_manager, tmp_path):
    """
    Test submitting an exercise updates the session and stats.
    """
    mock_user_id = 1
    session_manager.start_new_session(mock_user_id)

    # Mock stats_repository to prevent ZeroDivisionError
    session_manager.stats_repository.create_or_update_stats = MagicMock()

    # Create a temporary file to simulate the submitted exercise
    exercise_file = tmp_path / "exercise.py"
    exercise_file.write_text("print('Hello, world!')")

    session_manager.last_generated_file = str(exercise_file)

    feedback = session_manager.submit_exercise(mock_user_id)

    # Verify feedback and session updates
    assert feedback == "Exercise was correct! +10 points."
    assert session_manager.current_session.score == 10
    assert session_manager.current_session.successful_exercises == 1
    assert session_manager.current_session.exercises_completed == 1

    # Verify stats update
    session_manager.stats_repository.create_or_update_stats.assert_called_once_with(mock_user_id)


def test_submit_exercise_handles_file_not_found(session_manager):
    """
    Test submitting an exercise with a missing file raises an error.
    """
    mock_user_id = 1
    session_manager.start_new_session(mock_user_id)

    session_manager.last_generated_file = "non_existent_file.py"

    with pytest.raises(FileNotFoundError):
        session_manager.submit_exercise(mock_user_id)


def test_update_score_session_correctly_updates_score(session_manager):
    """
    Test updating the score based on the analysis result.
    """
    mock_user_id = 1
    session_manager.start_new_session(mock_user_id)

    feedback = session_manager._update_score_session("Result: True")
    assert feedback == "Exercise was correct! +10 points."
    assert session_manager.current_session.score == 10
    assert session_manager.current_session.successful_exercises == 1
    assert session_manager.current_session.exercises_completed == 1

    feedback = session_manager._update_score_session("Result: False")
    assert feedback == "Exercise was incorrect. No points awarded."
    assert session_manager.current_session.score == 10  # Score shouldn't change
    assert session_manager.current_session.successful_exercises == 1  # No increment
    assert session_manager.current_session.exercises_completed == 2
