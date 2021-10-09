from datetime import datetime

import pytest

from backend.models.auth import User, UserInDb
from backend.repositories.user_repository import UserRepository


@pytest.fixture
def mock_user() -> User:
    return User(username='test', joined_at=datetime(2021, 10, 10, 0, 0, 0))


@pytest.fixture
def mock_user_in_db(mock_user: User) -> UserInDb:
    return UserInDb(token='test', hashed_password='test', **mock_user.dict())


class TestUserRepository:

    def test_add(self, mock_user_repo: UserRepository, mock_user_in_db: UserInDb):
        mock_user_repo._add(mock_user_in_db)

    def test_get_user(self, mock_user_repo: UserRepository, mock_user_in_db: UserInDb):
        mock_user_repo._add(mock_user_in_db)
        user = mock_user_repo.get_user(mock_user_in_db.username)
        assert user.dict() == {
            'username': 'test',
            'joined_at': datetime(2021, 10, 10, 0, 0, 0)
        }

    def test_get_user_not_exists(self, mock_user_repo: UserRepository):
        user = mock_user_repo.get_user(username='test')
        assert user is None

    def test_get_token(self, mock_user_repo: UserRepository, mock_user_in_db: UserInDb):
        mock_user_repo._add(mock_user_in_db)
        token = mock_user_repo.get_token(mock_user_in_db.username)
        assert token == 'test'

    def test_get_token_not_exists(self, mock_user_repo: UserRepository):
        token = mock_user_repo.get_token(username='test')
        assert token is None

    def test_get_hashed_password(self, mock_user_repo: UserRepository, mock_user_in_db: UserInDb):
        mock_user_repo._add(mock_user_in_db)
        hashed_password = mock_user_repo.get_token(mock_user_in_db.username)
        assert hashed_password == 'test'

    def test_get_hashed_password_not_exists(self, mock_user_repo: UserRepository):
        hashed_password = mock_user_repo.get_hashed_password(username='test')
        assert hashed_password is None
