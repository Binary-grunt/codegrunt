import time
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from config.settings import settings


def wait_for_db():
    """
    Wait for the database to be ready.
    """
    engine = create_engine(settings.DATABASE_URL)
    print("Waiting for the database to be ready...")
    while True:
        try:
            # Test de la connexion
            with engine.connect():
                print("Database is ready!")
                break
        except OperationalError:
            print("Database is not ready yet, retrying...")
            time.sleep(1)
