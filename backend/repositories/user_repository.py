from contextlib import closing
from sqlite3 import Connection
from typing import Optional

from backend.models.auth import User, UserInDb
from backend.repositories.abstract import AbstractRepository


class UserRepository(AbstractRepository):

    def __init__(self, conn: Connection) -> None:
        self._conn = conn
        self._init_db()

    def _init_db(self) -> None:
        try:
            with closing(self._conn.cursor()) as cursor:
                query = """CREATE TABLE IF NOT EXISTS users
                           (id INTEGER PRIMARY KEY,
                            username VARCHAR (64) UNIQUE,
                            token VARCHAR (128) UNIQUE,
                            hashed_password VARCHAR (128),
                            joined_at VARCHAR (128));"""
                cursor.execute(query)
                self._conn.commit()
        except Exception as e:
            print('Exception arose:', e)
            raise

    def get_user(self, username: str) -> Optional[User]:
        try:
            with closing(self._conn.cursor()) as cursor:
                query = """SELECT joined_at FROM users
                           WHERE username = ?;"""
                cursor.execute(query, (username, ))

                if data := cursor.fetchone():
                    return User(username=username, joined_at=data[0])

        except Exception as e:
            print('Exception arose:', e)

    def get_hashed_password(self, username: str) -> Optional[str]:
        try:
            with closing(self._conn.cursor()) as cursor:
                query = """SELECT hashed_password FROM users
                           WHERE username = ?;"""
                cursor.execute(query, (username, ))

                if data := cursor.fetchone():
                    return data[0]

        except Exception as e:
            print('Exception arose:', e)
            raise

    def get_token(self, username: str) -> Optional[str]:
        try:
            with closing(self._conn.cursor()) as cursor:
                query = """SELECT token FROM users
                           WHERE username = ?;"""
                cursor.execute(query, (username, ))

                data = cursor.fetchone()
                if data is None:
                    return None

                token = data[0]
                return token

        except Exception as e:
            print('Exception arose:', e)
            raise

    def _add(self, user: UserInDb) -> None:
        try:
            with closing(self._conn.cursor()) as cursor:
                query = """INSERT INTO users (username, token, hashed_password, joined_at)
                           VALUES (?, ?, ?, ?);"""
                cursor.execute(query, (
                    user.username,
                    user.token,
                    user.hashed_password,
                    user.joined_at
                ))
                self._conn.commit()
        except Exception as e:
            print('Exception arose:', e)
            raise

    def _add_bulk(self, users: list[UserInDb]) -> None:
        pass
