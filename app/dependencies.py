from sqlalchemy.orm import Session
from db.database import SessionLocal, engine

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()