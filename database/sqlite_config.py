from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import settings

# Create the database engine
engine = create_engine(settings.DATABASE_URL, echo=True)

# Create a session local
SessionLocal = sessionmaker(bind=engine)
