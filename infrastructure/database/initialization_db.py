from .models import Base
from .sqlite_config import engine


def initialization_db():
    """
    Initialize the database by creating all tables.
    """
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully.")
