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
        Only sets attributes; delegates key loading and client initialization to other methods.
        """
        load_dotenv()  # Load environment variables from .env file
        self.api_key = api_key or self._load_api_key()
        self.client = self._setup_client()

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
            client = OpenAI(api_key=self.api_key)
            # Validate the client by making a test request (e.g., list models)
            client.models.list()
            return client
        except Exception as e:
            raise ValueError(f"Failed to initialize OpenAI client: {e}")

    def get_client(self) -> OpenAI:
        """
        Returns the OpenAI client instance.
        """
        return self.client
