import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration settings for the application


class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///code_grunt.db")


settings = Settings()
