from contextlib import closing
from sqlite3 import Connection
from typing import Optional

from backend.repositories.abstract import AbstractRepository
from backend.models.auth import UserInDb


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

    def get_hashed_password(self, username: str) -> Optional[str]:
        try:
            with closing(self._conn.cursor()) as cursor:
                query = f"""SELECT hashed_password FROM users
                            WHERE username = '{username}';"""
                cursor.execute(query)

                data = cursor.fetchone()
                if data is None:
                    return None

                hashed_password = data[0]
                return hashed_password

        except Exception as e:
            print('Exception arose:', e)
            raise

    def get_token(self, username: str) -> Optional[str]:
        try:
            with closing(self._conn.cursor()) as cursor:
                query = f"""SELECT token FROM users
                            WHERE username = '{username}';"""
                cursor.execute(query)

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
                query = f"""INSERT INTO users (username, token, hashed_password, joined_at)
                            VALUES ('{user.username}', '{user.token}', '{user.hashed_password}', '{user.joined_at}');"""
                cursor.execute(query)
                self._conn.commit()
        except Exception as e:
            print('Exception arose:', e)
            raise

    def _add_bulk(self, users: list[UserInDb]) -> None:
        pass
