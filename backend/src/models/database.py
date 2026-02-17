from sqlmodel import Session, create_engine
from src.config import DATABASE_URL
from typing import Generator

# Create the database engine
engine = create_engine(DATABASE_URL, echo=True)

def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session