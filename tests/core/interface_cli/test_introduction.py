import pytest
from rich.console import Console
from io import StringIO
from core.interface_cli.introduction import Introduction


@pytest.fixture
def mock_console_output():
    """
    Fixture to capture the console output using a StringIO buffer.
    """
    buffer = StringIO()
    console = Console(file=buffer, force_terminal=True)
    return console, buffer


def test_display_introduction(mock_console_output):
    """
    Test the Introduction.display method for correct structure and content.
    """
    # Use the real Console but redirect its output to the mock buffer
    console, buffer = mock_console_output

    # Patch the Console instance used in Introduction
    with pytest.MonkeyPatch.context() as monkeypatch:
        monkeypatch.setattr("core.interface_cli.introduction.Console", lambda: console)

        # Call the display method
        Introduction.display()

    # Retrieve the output from the buffer
    output = buffer.getvalue()

    # Assertions for expected content in the output
    assert "Welcome to the Codegrunt" in output
    assert "Generating coding exercises based on your preferences" in output
    assert "Improve your skills one exercise at a time!" in output
    assert "Menu Options:" in output
    assert "Generate an exercise: Create a new coding challenge" in output
    assert "Happy Coding! Let's tackle those coding challenges together!" in output
