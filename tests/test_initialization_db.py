from sqlalchemy import inspect
from database import initialization_db, engine
from database.models import Base


def test_init_db():
    """
    Test the initialization of the database.
    """
    # Delete all tables from the database
    Base.metadata.drop_all(bind=engine)

    # Call the initialization function
    initialization_db()

    # Inspect the database to get all table names
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    # Check that the expected tables are present
    expected_tables = ["users", "sessions", "stats"]  # Expected tables
    for table in expected_tables:
        assert table in tables
