import secrets
import sqlite3
import hashlib
from datetime import datetime
from typing import Optional

from backend.config import Config
from backend.models.auth import UserInDb
from backend.repositories.user_repository import UserRepository


def hash_password(password: str) -> str:
    password, salt = map(lambda item: item.encode(), (password, Config().salt))
    return hashlib.sha512(password + salt).hexdigest()


def login_user(username: str, password: str) -> Optional[str]:
    conn = sqlite3.connect(Config().db_path)
    repo = UserRepository(conn)

    expected_hashed_password = repo.get_hashed_password(username)
    if check_password(password, expected_hashed_password):
        return repo.get_token(username)


def create_user(username: str, password: str) -> Optional[str]:
    conn = sqlite3.connect(Config().db_path)
    repo = UserRepository(conn)

    if check_if_user_exists(username, repo):
        return None

    token = secrets.token_hex()
    user_in_db = UserInDb(username=username,
                          joined_at=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                          hashed_password=hash_password(password),
                          token=token)
    repo._add(user_in_db)
    return token


def check_password(password: str, expected_hashed_password: str) -> bool:
    hashed_password = hash_password(password)
    return hashed_password == expected_hashed_password


def check_if_user_exists(username: str, repo: UserRepository) -> bool:
    return repo.get_user(username) is not None
