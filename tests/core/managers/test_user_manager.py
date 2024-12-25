import pytest
from unittest.mock import MagicMock
from core.managers.user_manager import UserManager
from database.models import User


@pytest.fixture
def mock_session_manager():
    """
    Fixture to mock the SessionManager and its user_repository dependency.
    """
    session_manager = MagicMock()
    session_manager.user_repository = MagicMock()
    return session_manager


def test_get_or_create_user_creates_new_user(mock_session_manager):
    """
    Test get_or_create_user creates a new user when no user exists in the database.
    """
    # Arrange: Mock the behavior of user_repository to return None for get_first_user
    mock_session_manager.user_repository.get_first_user.return_value = None

    # Create a mock user for the add_user method
    new_user = MagicMock(spec=User)
    new_user.id = 1
    mock_session_manager.user_repository.add_user.return_value = new_user

    user_manager = UserManager(mock_session_manager)

    # Act: Call get_or_create_user
    user = user_manager.get_or_create_user()

    # Assert: Ensure a new user is created and returned
    mock_session_manager.user_repository.get_first_user.assert_called_once()
    mock_session_manager.user_repository.add_user.assert_called_once()
    assert user.id == 1
    assert user == new_user


def test_get_or_create_user_retrieves_existing_user(mock_session_manager):
    """
    Test get_or_create_user retrieves an existing user if one exists in the database.
    """
    # Arrange: Mock the behavior of user_repository to return an existing user
    existing_user = MagicMock(spec=User)
    existing_user.id = 42
    mock_session_manager.user_repository.get_first_user.return_value = existing_user

    user_manager = UserManager(mock_session_manager)

    # Act: Call get_or_create_user
    user = user_manager.get_or_create_user()

    # Assert: Ensure the existing user is retrieved
    mock_session_manager.user_repository.get_first_user.assert_called_once()
    mock_session_manager.user_repository.add_user.assert_not_called()
    assert user.id == 42
    assert user == existing_user
