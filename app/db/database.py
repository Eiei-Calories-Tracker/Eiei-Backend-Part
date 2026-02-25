from sqlmodel import SQLModel, create_engine, Session
from core.config import DATABASE_URL

# Create engine for PostgreSQL
engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    """Create all tables in the database"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Dependency to get database session"""
    with Session(engine) as session:
        yield session