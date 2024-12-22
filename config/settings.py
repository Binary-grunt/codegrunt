import os
from dotenv import load_dotenv


class Settings:
    """
    Application-wide configuration settings.
    """

    def __init__(self, load_env=True):
        if load_env:
            load_dotenv()
        self.DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///code_grunt.db")
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


settings = Settings()
