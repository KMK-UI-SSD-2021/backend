from contextlib import closing
from sqlite3 import Connection

from backend.models.lobby import Lobby, Settings
from backend.repositories.abstract import AbstractRepository


class LobbyRepository(AbstractRepository):

    def __init__(self, conn: Connection) -> None:
        self._conn = conn
        self._init_db()

    def _init_db(self) -> None:
        try:
            with closing(self._conn.cursor()) as cursor:
                query = """CREATE TABLE IF NOT EXISTS lobbies
                           (id INTEGER PRIMARY KEY,
                            owner VARCHAR (64),
                            name VARCHAR (32),
                            settings VARCHAR (1024));"""
                cursor.execute(query)
                self._conn.commit()

        except Exception as e:  # pragma: no cover
            print('Exception arose:', e)
            raise

    def get(self, lobby_id: int) -> Lobby:
        try:
            with closing(self._conn.cursor()) as cursor:
                query = """SELECT owner, name, settings FROM lobbies
                           WHERE id = ?;"""
                cursor.execute(query, (lobby_id, ))

                lobby_data = cursor.fetchone()
                if not lobby_data:
                    return None

                owner, name, settings = lobby_data
                return Lobby(owner=owner,
                             name=name,
                             settings=Settings.parse_raw(settings))

        except Exception as e:  # pragma: no cover
            print('Exception arose:', e)
            raise

    def _add(self, lobby: Lobby) -> int:
        try:
            with closing(self._conn.cursor()) as cursor:
                query = """INSERT INTO lobbies (owner, name, settings)
                           VALUES (?, ?, ?);"""
                cursor.execute(query, (
                    lobby.owner,
                    lobby.name,
                    lobby.settings.json()
                ))

                self._conn.commit()
                return cursor.lastrowid

        except Exception as e:  # pragma: no cover
            print('Exception arose:', e)
            raise

    def _add_bulk(self, lobbies: list[Lobby]) -> None:  # pragma: no cover
        pass
