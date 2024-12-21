import pytest
from unittest.mock import MagicMock
from api.openai_prompt import OpenAIPrompt


@pytest.fixture
def mock_openai_client():
    """
    Fixture to provide a mocked OpenAI client.
    """
    return MagicMock()


@pytest.fixture
def openai_prompt(mock_openai_client):
    """
    Fixture to provide an instance of OpenAIPrompt with a mocked OpenAI client.
    """
    return OpenAIPrompt(client=mock_openai_client)


def test_generate_exercise_success(openai_prompt, mock_openai_client):
    """
    Test generating an exercise successfully.
    """
    mock_openai_client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content="Generated exercise code"))]
    )

    subject = "variables"
    language = "Python"
    result = openai_prompt.generate_exercise(subject, language)

    assert result == "Generated exercise code"
    mock_openai_client.chat.completions.create.assert_called_once()
    assert "variables" in mock_openai_client.chat.completions.create.call_args[1]["messages"][1]["content"]
    assert "Python" in mock_openai_client.chat.completions.create.call_args[1]["messages"][1]["content"]


def test_analyze_code_success(openai_prompt, mock_openai_client):
    """
    Test analyzing code successfully.
    """
    mock_openai_client.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content="Result: True"))]
    )

    file_content = "def add(a, b): return a + b"
    result = openai_prompt.analyze_code(file_content)

    assert result == "Result: True"
    mock_openai_client.chat.completions.create.assert_called_once()
    assert file_content in mock_openai_client.chat.completions.create.call_args[1]["messages"][1]["content"]


def test_generate_exercise_failure(openai_prompt, mock_openai_client):
    """
    Test generating an exercise when an API error occurs.
    """
    mock_openai_client.chat.completions.create.side_effect = Exception("API error")

    subject = "variables"
    language = "Python"
    result = openai_prompt.generate_exercise(subject, language)

    assert "An error occurred: API error" in result


def test_analyze_code_failure(openai_prompt, mock_openai_client):
    """
    Test analyzing code when an API error occurs.
    """
    mock_openai_client.chat.completions.create.side_effect = Exception("API error")

    file_content = "def add(a, b): return a + b"
    result = openai_prompt.analyze_code(file_content)

    assert "An error occurred: API error" in result
