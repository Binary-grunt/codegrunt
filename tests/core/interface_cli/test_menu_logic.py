import pytest
from unittest.mock import MagicMock
from rich.console import Console
from typer import Exit
from core.interface_cli.menu_logic import MenuLogic


@pytest.fixture
def mock_dependencies():
    """
    Fixture to create mocked dependencies for MenuLogic.
    """
    mock_console = MagicMock(spec=Console)
    mock_preference_manager = MagicMock()
    mock_session_manager = MagicMock()
    mock_user_manager = MagicMock()

    # Set up mock preferences
    mock_preference_manager.get_preferences.return_value = ("python", "OOP", "beginner")

    # Set up mock user
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user_manager.get_or_create_user.return_value = mock_user

    # Set up session manager
    mock_session_manager.generate_exercise.return_value = "/path/to/generated/file.py"
    mock_session_manager.last_generated_file = "/path/to/last/generated/file.py"
    mock_session_manager.submit_exercise.return_value = "Solution submitted successfully!"
    mock_session_manager.current_session = None  # No active session initially

    # Mock stats repository with realistic attributes
    mock_stats = MagicMock(total_sessions=5, total_exercises=15, average_score=88.5)
    mock_session_manager.stats_repository.get_stats_by_user.return_value = mock_stats

    return mock_console, mock_preference_manager, mock_session_manager, mock_user_manager


def test_handle_choice_pre_exercise(mock_dependencies):
    """
    Test handle_choice_pre_exercise with different choices.
    """
    console, preference_manager, session_manager, user_manager = mock_dependencies
    menu_logic = MenuLogic(console, preference_manager, session_manager, user_manager)

    # Test choice "1" (generate exercise)
    menu_logic.handle_choice_pre_exercise("1")
    session_manager.generate_exercise.assert_called_once_with(
        user_id=1, language="python", subject="OOP", level="beginner"
    )
    console.print.assert_any_call("\n[blue]Generating a new exercise...[/blue]")

    # Test choice "2" (view global stats)
    # Simulate no stats available
    session_manager.stats_repository.get_stats_by_user.return_value = None
    menu_logic.handle_choice_pre_exercise("2")
    console.print.assert_any_call("[yellow]No global stats available yet.[/yellow]")  # Correct assertion for empty stats


def test_handle_choice_post_exercise(mock_dependencies):
    """
    Test handle_choice_post_exercise with different choices.
    """
    console, preference_manager, session_manager, user_manager = mock_dependencies
    menu_logic = MenuLogic(console, preference_manager, session_manager, user_manager)

    # Test choice "1" (run solution)
    menu_logic.handle_choice_post_exercise("1")
    console.print.assert_any_call("\n[blue]Running your solution for testing...[/blue]")
    console.print.assert_any_call(
        f"[yellow]Running the file: {session_manager.last_generated_file}[/yellow]"
    )

    # Test choice "2" (submit solution)
    menu_logic.handle_choice_post_exercise("2")
    session_manager.submit_exercise.assert_called_once_with(user_id=1)

    # Test choice "3" (view session stats)
    session_manager.current_session = None  # Explicitly set to None
    menu_logic.handle_choice_post_exercise("3")
    console.print.assert_any_call("[yellow]No active session. Please generate an exercise to start a session.[/yellow]")  # Correct assertion for no session

    # Test choice "5" (exit)
    with pytest.raises(Exit):
        menu_logic.handle_choice_post_exercise("5")
    console.print.assert_any_call("[red]Exiting the application... Goodbye![/red]")

    # Test invalid choice
    menu_logic.handle_choice_post_exercise("invalid")
    console.print.assert_any_call("[yellow]Invalid choice. Please select a valid option.[/yellow]")
