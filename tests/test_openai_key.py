import pytest
from config.settings import settings
from api.openai_key import OpenAIKey


@pytest.fixture
def mock_settings(monkeypatch):
    """
    Fixture to mock the settings with environment variables.
    """
    monkeypatch.setattr(settings, "OPENAI_API_KEY", "mock-api-key")


def test_openai_key_initialization_with_env(mock_settings):
    """
    Test initialization of OpenAIKey with an API key loaded from settings.
    """
    openai_key = OpenAIKey()
    assert openai_key.api_key == "mock-api-key", "API key should be loaded from settings"


def test_openai_key_initialization_with_explicit_key():
    """
    Test initialization of OpenAIKey with an explicitly provided API key.
    """
    openai_key = OpenAIKey(api_key="explicit-key")
    assert openai_key.api_key == "explicit-key", "API key should match the explicitly provided value"


def test_openai_key_missing_env(monkeypatch):
    """
    Test behavior when the API key is missing from settings.
    """
    monkeypatch.setattr(settings, "OPENAI_API_KEY", None)

    with pytest.raises(ValueError, match="API key is missing. Please set it in the environment or .env file."):
        OpenAIKey()
