import pytest
from unittest.mock import patch, MagicMock
from api.openai_service import OpenAIService
from api.openai_key import OpenAIKey
from patterns.decorators import SingletonMeta


@pytest.fixture
def mock_openai_key(monkeypatch):
    """
    Fixture to mock OpenAIKey with a valid API key.
    """
    monkeypatch.setattr(OpenAIKey, "api_key", "mock-api-key")


@patch("api.openai_service.OpenAI")
def test_openai_service_initialization(mock_openai, mock_openai_key):
    """
    Test the initialization of OpenAIService with a valid API key and client setup.
    """
    # Reset the singleton instance cache
    SingletonMeta.reset_instances()
    # Mock OpenAI client
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    mock_client.models.list.return_value = ["mock-model"]

    # Initialize OpenAIService
    service = OpenAIService()

    # Verify client initialization and model setup
    assert service.model == OpenAIService.DEFAULT_MODEL
    mock_client.models.list.assert_called_once()


@patch("api.openai_service.OpenAI")
def test_openai_service_request_response(mock_openai, mock_openai_key):
    """
    Test the request_response_to_openai method.
    """

    # Reset the singleton instance cache
    SingletonMeta.reset_instances()

    # Mock OpenAI client and response
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="Mock response"))]
    mock_client.chat.completions.create.return_value = mock_response

    # Initialize OpenAIService
    service = OpenAIService()

    # Test sending a request
    messages = [{"role": "user", "content": "Test message"}]
    response = service.request_response_to_openai(messages)

    # Verify the response
    assert response == "Mock response"
    mock_client.chat.completions.create.assert_called_once_with(model=service.model, messages=messages)


@patch("api.openai_service.OpenAI")
def test_openai_service_initialization_failure(mock_openai, mock_openai_key):
    """
    Test behavior when OpenAI client initialization fails.
    """

    # Reset the singleton instance cache
    SingletonMeta.reset_instances()
    # Simulate failure during client setup
    mock_openai.return_value.models.list.side_effect = Exception("Client setup failed")

    with pytest.raises(ValueError, match="Failed to initialize OpenAI client: Client setup failed"):
        OpenAIService()


@patch("api.openai_service.OpenAI")
def test_openai_service_request_failure(mock_openai, mock_openai_key):
    """
    Test behavior when the request to OpenAI fails.
    """

    # Reset the singleton instance cache
    SingletonMeta.reset_instances()
    # Mock OpenAI client
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    mock_client.chat.completions.create.side_effect = Exception("API request failed")

    # Initialize OpenAIService
    service = OpenAIService()

    # Test sending a request
    messages = [{"role": "user", "content": "Test message"}]
    with pytest.raises(ValueError, match="Failed to process the request: API request failed"):
        service.request_response_to_openai(messages)
