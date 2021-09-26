import hashlib

from backend.config import Config


def hash_password(password: str) -> str:
    password, salt = map(lambda item: item.encode(), (password, Config().salt))
    return hashlib.sha512(password + salt).hexdigest()


def check_password(password: str, expected_hashed_password: str) -> bool:
    hashed_password = hash_password(password)
    return hashed_password == expected_hashed_password
