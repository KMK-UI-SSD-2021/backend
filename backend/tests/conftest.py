import sqlite3

import pytest
from starlette.testclient import TestClient

from backend.api.asgi import app
from backend.models.lobby import Image, Settings
from backend.repositories.lobby_repository import LobbyRepository
from backend.repositories.statistics_repository import StatisticsRepository
from backend.repositories.user_repository import UserRepository


@pytest.fixture
def mock_db_conn() -> sqlite3.Connection:
    yield sqlite3.connect(':memory:')


@pytest.fixture
def mock_user_repo(mock_db_conn: sqlite3.Connection) -> UserRepository:
    return UserRepository(mock_db_conn)


@pytest.fixture
def mock_lobby_repo(mock_db_conn: sqlite3.Connection) -> LobbyRepository:
    return LobbyRepository(mock_db_conn)


@pytest.fixture
def mock_statistics_repo(mock_db_conn: sqlite3.Connection) -> StatisticsRepository:
    return StatisticsRepository(mock_db_conn)


@pytest.fixture
def mock_client(mock_user_repo: UserRepository,
                mock_lobby_repo: LobbyRepository,
                mock_statistics_repo: StatisticsRepository) -> TestClient:
    app.state.user_repo = mock_user_repo
    app.state.lobby_repo = mock_lobby_repo
    app.state.statistics_repo = mock_statistics_repo
    yield TestClient(app)


@pytest.fixture
def mock_settings() -> Settings:
    return Settings(images_batch=2,
                    images=[Image(url='https://imgur.com/1'),
                            Image(url='https://imgur.com/2')],
                    tags=['test1', 'test2'])
