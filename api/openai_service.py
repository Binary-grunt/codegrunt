from openai import OpenAI
from common.decorators import singleton
from api.openai_key import OpenAIKey


@singleton
class OpenAIService:
    """
    A Singleton service class to manage all interactions with the OpenAI API.
    """
    DEFAULT_MODEL = "gpt-4o-mini"

    def __init__(self, model: str = None):
        """
        Initializes the OpenAIService with the OpenAI client and model.
        """
        self.model = model or self.DEFAULT_MODEL
        self._client = self._setup_client()

    def _setup_client(self) -> OpenAI:
        """
        Initializes and validates the OpenAI client.
        """
        try:
            api_key = OpenAIKey().api_key  # Fetch API key from OpenAIKey
            client = OpenAI(api_key=api_key)
            client.models.list()  # Validate the client by listing models
            return client
        except Exception as e:
            raise ValueError(f"Failed to initialize OpenAI client: {e}")

    def request_response_to_openai(self, messages: list[dict]) -> str:
        """
        Sends a message to the OpenAI API and returns the response.

        Args:
            messages (list[dict]): A list of message dictionaries for the OpenAI chat API.

        Returns:
            str: The content of the first message in the response.
        """
        try:
            completion = self._client.chat.completions.create(model=self.model, messages=messages)
            return completion.choices[0].message.content
        except Exception as e:
            raise ValueError(f"Failed to process the request: {e}")
