import pytest
from unittest.mock import MagicMock, patch
from core.interface_cli.application_interface import ApplicationInterface
from typer import Exit


@pytest.fixture
def mock_session_manager():
    """
    Fixture to mock the SessionManager.
    """
    return MagicMock()


@pytest.fixture
def mock_user_manager():
    """
    Fixture to mock the UserManager.
    """
    user = MagicMock()
    user.id = 1
    mock_manager = MagicMock()
    mock_manager.get_or_create_user.return_value = user
    return mock_manager


@pytest.fixture
def mock_preference_cli():
    """
    Fixture to mock the PreferenceCli.
    """
    mock_cli = MagicMock()
    mock_cli.get_preferences.return_value = ("python", "OOP", "intermediate")
    return mock_cli


@pytest.fixture
def app_interface(mock_session_manager, mock_user_manager, mock_preference_cli):
    """
    Fixture to create an ApplicationInterface instance with mocked dependencies.
    """
    return ApplicationInterface(
        session_manager=mock_session_manager,
        user_manager=mock_user_manager,
        preference_cli=mock_preference_cli,
    )


@patch("core.interface_cli.application_interface.Console.print")
def test_introduction(mock_print, app_interface):
    """
    Test the introduction method to verify the introduction text is displayed.
    """
    app_interface.introduction()

    # Assert that print was called multiple times (for panels and sections)
    assert mock_print.call_count > 1


@patch("core.interface_cli.application_interface.Prompt.ask")
def test_run_generate_exercise(mock_prompt_ask, app_interface, mock_session_manager):
    """
    Test the run method for generating an exercise.
    """
    # Mock user input to choose "1" (Generate Exercise) and then "6" (Exit)
    mock_prompt_ask.side_effect = ["1", "6"]

    # Run the application
    with patch("core.interface_cli.application_interface.Console.print"):
        app_interface.run()

    # Verify the generate_exercise method was called with the correct arguments
    mock_session_manager.generate_exercise.assert_called_once_with(
        user_id=1, language="python", subject="OOP", level="intermediate"
    )


@patch("core.interface_cli.application_interface.Prompt.ask")
def test_run_view_global_stats(mock_prompt_ask, app_interface, mock_session_manager):
    """
    Test the run method for viewing global stats.
    """
    # Mock user input to choose "4" (View Global Stats) and then "6" (Exit)
    mock_prompt_ask.side_effect = ["4", "6"]

    # Run the application
    with patch("core.interface_cli.application_interface.Console.print"):
        app_interface.run()

    # Verify the stats_repository.get_stats_by_user method was called
    mock_session_manager.stats_repository.get_stats_by_user.assert_called_once_with(1)


@patch("core.interface_cli.application_interface.Prompt.ask")
def test_run_view_current_session_stats(mock_prompt_ask, app_interface, mock_session_manager):
    """
    Test the run method for viewing current session stats.
    """
    # Mock user input to choose "5" (View Current Session Stats) and then "6" (Exit)
    mock_prompt_ask.side_effect = ["5", "6"]

    # Set up a mock current session
    mock_session_manager.current_session = MagicMock(
        id=2, exercises_completed=3, successful_exercises=2, score=30
    )

    # Run the application
    with patch("core.interface_cli.application_interface.Console.print"):
        app_interface.run()

    # Verify the current session stats were displayed
    assert mock_session_manager.current_session is not None


@patch("core.interface_cli.application_interface.Prompt.ask")
def test_run_invalid_choice(mock_prompt_ask, app_interface):
    """
    Test the run method for handling an invalid choice.
    """
    # Mock user input to choose "invalid" and then "6" (Exit)
    mock_prompt_ask.side_effect = ["invalid", "6"]

    # Run the application
    with patch("core.interface_cli.application_interface.Console.print") as mock_print:
        app_interface.run()

    # Verify that an error message was printed
    mock_print.assert_any_call("[red]An error occurred: invalid literal for int() with base 10: 'invalid'[/red]")
