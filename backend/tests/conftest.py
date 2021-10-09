import sqlite3

import pytest
from starlette.testclient import TestClient

from backend.api.asgi import app
from backend.repositories.user_repository import UserRepository


@pytest.fixture
def mock_db_conn() -> sqlite3.Connection:
    yield sqlite3.connect(':memory:')


@pytest.fixture
def mock_user_repo(mock_db_conn: sqlite3.Connection) -> UserRepository:
    return UserRepository(mock_db_conn)


@pytest.fixture
def mock_client(mock_user_repo: UserRepository) -> TestClient:
    app.state.user_repo = mock_user_repo
    yield TestClient(app)
