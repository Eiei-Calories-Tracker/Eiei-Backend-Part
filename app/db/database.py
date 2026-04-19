from sqlmodel import SQLModel, create_engine, Session
from core.config import DATABASE_URL

from sqlalchemy.orm import sessionmaker

# Create engine for PostgreSQL
engine = create_engine(DATABASE_URL, echo=True)

# SessionLocal for traditional session handling
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_db_and_tables():
    """Create all tables in the database"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Dependency to get database session"""
    with Session(engine) as session:
        yield session