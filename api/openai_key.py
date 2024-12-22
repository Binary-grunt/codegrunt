class OpenAIKey:
    """
    A Class to manage the OpenAI API key.
    """

    def __init__(self, api_key: str = None):
        """
        Initializes the OpenAIKey instance with an API key.
        """
        self._api_key = api_key or self._load_api_key()

    def _load_api_key(self) -> str:
        """
        Loads the OpenAI API key from the settings.
        """
        from config.settings import settings  # Import here to avoid circular imports
        api_key = settings.OPENAI_API_KEY
        if not api_key:
            raise ValueError("API key is missing. Please set it in the environment or .env file.")
        return api_key

    @property
    def api_key(self) -> str:
        """
        Getter for the API key.
        """
        return self._api_key
