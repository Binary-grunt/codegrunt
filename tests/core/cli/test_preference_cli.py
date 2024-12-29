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
    Test the set_preferences method with mocked user input, including fuzzy matching.
    """
    # Arrange: Provide four responses (language, subject, confirmation, level)
    mock_prompt_ask.side_effect = [
        "python",        # 1) Language
        "dat_structr",   # 2) Subject (will be fuzzy matched to "data_structures")
        "yes",           # 3) Confirm the suggested subject
        "intermediate",  # 4) Difficulty level
    ]

    # Act: Call the set_preferences method
    preference_cli.set_preferences()

    # Assert: Ensure the preferences were set correctly
    assert preference_cli.language == "python"
    assert preference_cli.subject == "data_structures"  # Corrected via fuzzy matching
    assert preference_cli.level == "intermediate"

    # Optional: Verify all expected Prompt.ask calls were indeed made
    mock_prompt_ask.assert_any_call(
        "[bold green]Enter the programming language[/bold green] (e.g., python, cpp, java)"
    )
    mock_prompt_ask.assert_any_call(
        "[bold green]Enter the subject[/bold green] (e.g., OOP, data_structures)"
    )
    mock_prompt_ask.assert_any_call(
        "[bold green]Confirm subject?[/bold green] (yes/no)",
        choices=["yes", "no"],
        default="yes"
    )
    mock_prompt_ask.assert_any_call(
        "[bold green]Enter the difficulty level[/bold green]",
        choices=["beginner", "intermediate", "advanced", "expert"],  # update if needed
        default="beginner"
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
    # Provide four responses (language, subject, confirmation, level)
    # Even though 'data_structures' is already correct, fuzzy matching
    # will still ask for confirmation.
    mock_prompt_ask.side_effect = [
        "cpp",              # 1) Language
        "data_structures",  # 2) Subject
        "yes",              # 3) Confirm subject
        "advanced",         # 4) Difficulty level
    ]

    # Act: Set preferences and then retrieve them
    preference_cli.set_preferences()
    language, subject, level = preference_cli.get_preferences()

    # Assert: Ensure the retrieved preferences match the set preferences
    assert language == "cpp"
    assert subject == "data_structures"
    assert level == "advanced"
