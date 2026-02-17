import pytest
from sqlmodel import create_engine, SQLModel
from sqlmodel.pool import StaticPool
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker

from src.main import app
from src.models.database import get_session


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    session = sessionmaker(engine)()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(name="client")
def client_fixture(session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()