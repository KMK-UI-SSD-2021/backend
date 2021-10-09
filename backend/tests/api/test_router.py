import sqlite3

import pytest
from starlette.testclient import TestClient

from backend.api.asgi import app
from backend.models.auth import UserInRequest
from backend.repositories.user_repository import UserRepository
from backend.services.auth import create_user


@pytest.fixture
def mock_user() -> UserInRequest:
    return UserInRequest(username='test', password='test')


@pytest.fixture
def mock_db_conn() -> sqlite3.Connection:
    yield sqlite3.connect(':memory:')


@pytest.fixture
def mock_client(mock_db_conn: sqlite3.Connection) -> TestClient:
    app.state.user_repo = UserRepository(mock_db_conn)
    yield TestClient(app)


class TestRegister:

    def test_register_new_user(self, mock_client: TestClient, mock_user: UserInRequest):
        response = mock_client.post('/api/v1/register', json=mock_user.dict())
        json_response = response.json()

        assert 'token' in json_response
        assert len(json_response['token']) == 64

    def test_register_user_exists(self, mock_client: TestClient, mock_user: UserInRequest):
        create_user(mock_client.app.state.user_repo, mock_user.username, mock_user.password)

        response = mock_client.post('/api/v1/register', json=mock_user.dict())
        json_response = response.json()

        assert 'error' in json_response
        assert json_response['error'] == 'user exists'


class TestLogin:

    def test_login_user_exists(self, mock_client: TestClient, mock_user: UserInRequest):
        create_user(mock_client.app.state.user_repo, mock_user.username, mock_user.password)

        response = mock_client.post('/api/v1/login', json=mock_user.dict())
        json_response = response.json()

        assert 'token' in json_response
        assert len(json_response['token']) == 64

    def test_login_not_exists(self, mock_client: TestClient, mock_user: UserInRequest):
        response = mock_client.post('/api/v1/login', json=mock_user.dict())
        json_response = response.json()

        assert 'error' in json_response
        assert json_response['error'] == 'wrong credentials'
