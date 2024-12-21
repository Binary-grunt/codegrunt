from patterns.decorators import singleton
import os
from openai import OpenAI
from dotenv import load_dotenv


@singleton
class OpenAIKey:
    """
    A Singleton class to manage the OpenAI API key and its client.
    """

    def __init__(self, api_key: str = None):
        """
        Initializes the OpenAIKey instance with an API key and sets up the client.
        """
        load_dotenv()  # Load environment variables from .env file
        self._api_key = api_key or self._load_api_key()
        self._client = self._setup_client()

    def _load_api_key(self) -> str:
        """
        Loads the OpenAI API key from the environment or raises an error if not found.
        """
        print("Calling _load_api_key")
        api_key = os.getenv("OPENAI_API_KEY")
        print(f"os.getenv returned: {api_key}")
        if not api_key:
            raise ValueError("API key is missing. Please set it in .env or provide it explicitly.")
        return api_key

    def _setup_client(self) -> OpenAI:
        """
        Sets up and returns the OpenAI client using the API key.
        """
        try:
            client = OpenAI(api_key=self._api_key)
            # Validate the client by making a test request (e.g., list models)
            client.models.list()
            return client
        except Exception as e:
            raise ValueError(f"Failed to initialize OpenAI client: {e}")

    @property
    def api_key(self) -> str:
        """
        Getter for the API key.
        """
        return self._api_key

    @api_key.setter
    def api_key(self, new_key: str):
        """
        Setter for the API key. Updates the key and reconfigures the client.
        """
        print(f"Updating API key to: {new_key}")
        if not new_key:
            raise ValueError("API key cannot be empty.")
        self._api_key = new_key
        self._client = self._setup_client()  # Reconfigure client with new key

    @property
    def client(self) -> OpenAI:
        """
        Getter for the OpenAI client.
        """
        return self._client
