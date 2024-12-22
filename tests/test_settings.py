import os
import pytest
from unittest.mock import patch
from config.settings import Settings


@pytest.fixture
def mock_env_variables(monkeypatch):
    """
    Fixture to mock environment variables.
    """
    monkeypatch.setenv("DATABASE_URL", "sqlite:///test_code_grunt.db")
    monkeypatch.setenv("OPENAI_API_KEY", "test-api-key")


def test_settings_with_env_variables(mock_env_variables):
    """
    Test the Settings class when environment variables are set.
    """
    settings = Settings(load_env=False)  # No need to load dotenv since we're mocking the env vars

    assert settings.DATABASE_URL == "sqlite:///test_code_grunt.db"
    assert settings.OPENAI_API_KEY == "test-api-key"


@patch.dict(os.environ, {}, clear=True)
def test_settings_without_env_variables():
    """
    Test the Settings class when no environment variables are set.
    """
    settings = Settings(load_env=False)

    # Default values should be used
    assert settings.DATABASE_URL == "sqlite:///code_grunt.db"
    assert settings.OPENAI_API_KEY is None


@patch("config.settings.load_dotenv")
def test_settings_load_env(mock_load_dotenv, monkeypatch):
    """
    Test the Settings class to ensure load_dotenv is called when load_env=True.
    """
    # Mock environment variables
    monkeypatch.setenv("DATABASE_URL", "sqlite:///test_loaded_dotenv.db")
    monkeypatch.setenv("OPENAI_API_KEY", "dotenv-api-key")

    settings = Settings(load_env=True)

    # Ensure load_dotenv was called
    mock_load_dotenv.assert_called_once()

    # Check that environment variables are loaded correctly
    assert settings.DATABASE_URL == "sqlite:///test_loaded_dotenv.db"
    assert settings.OPENAI_API_KEY == "dotenv-api-key"
