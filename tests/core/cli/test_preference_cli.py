import pytest
from unittest.mock import patch
from core.cli.preference_cli import PreferenceCli


@pytest.fixture
def preference_cli():
    """
    Fixture to create a PreferenceCli instance for testing.
    """
    return PreferenceCli()


@patch("core.cli.preference_cli.Prompt.ask")
def test_set_preferences(mock_prompt_ask, preference_cli):
    """
    Test the set_preferences method with mocked user input.
    """
    # Arrange: Mock the responses for Prompt.ask
    mock_prompt_ask.side_effect = ["python", "OOP", "intermediate"]

    # Act: Call the set_preferences method
    preference_cli.set_preferences()

    # Assert: Ensure the preferences were set correctly
    assert preference_cli.language == "python"
    assert preference_cli.subject == "OOP"
    assert preference_cli.level == "intermediate"
    mock_prompt_ask.assert_any_call(
        "[bold green]Enter the programming language[/bold green] (e.g., python, cpp, java)"
    )
    mock_prompt_ask.assert_any_call(
        "[bold green]Enter the subject[/bold green] (e.g., OOP, data_structures)"
    )
    mock_prompt_ask.assert_any_call(
        "[bold green]Enter the difficulty level[/bold green] (e.g., beginner/intermediate/advanced)",
        choices=["beginner", "intermediate", "advanced"],
        default="beginner",
    )


def test_get_preferences_without_setting(preference_cli, capsys):
    """
    Test get_preferences when preferences have not been set.
    """
    # Act: Call get_preferences without setting preferences
    language, subject, level = preference_cli.get_preferences()

    # Assert: Check that preferences are None and error message is displayed
    assert language is None
    assert subject is None
    assert level is None

    # Capture console output
    captured = capsys.readouterr()
    assert "Preferences have not been set. Please configure them first." in captured.out


@patch("core.cli.preference_cli.Prompt.ask")
def test_get_preferences_after_setting(mock_prompt_ask, preference_cli):
    """
    Test get_preferences after preferences have been set.
    """
    # Arrange: Mock the responses for Prompt.ask
    mock_prompt_ask.side_effect = ["cpp", "data_structures", "advanced"]

    # Act: Set preferences and then retrieve them
    preference_cli.set_preferences()
    language, subject, level = preference_cli.get_preferences()

    # Assert: Ensure the retrieved preferences match the set preferences
    assert language == "cpp"
    assert subject == "data_structures"
    assert level == "advanced"
