from contextlib import closing
from sqlite3 import Connection
from typing import Optional

from backend.repositories.abstract import AbstractRepository
from backend.models.base import GameLobby, GameSettings


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
        except Exception as e:
            print('Exception arose:', e)
            raise

    def get(self, id: int) -> GameLobby:
        try:
            with closing(self._conn.cursor()) as cursor:
                query = f"""SELECT owner, name, settings FROM lobbies
                            WHERE id = {id}"""
                cursor.execute(query)

                lobby_data = cursor.fetchone()
                if not lobby_data:
                    return None

                owner, name, settings = lobby_data
                return GameLobby(owner=owner,
                                 name=name,
                                 settings=GameSettings.parse_raw(settings))

        except Exception as e:
            print('Exception arose:', e)
            raise

    def _add(self, lobby: GameLobby) -> None:
        try:
            with closing(self._conn.cursor()) as cursor:
                query = f"""INSERT INTO lobbies (owner, name, settings)
                            VALUES ('{lobby.owner}', '{lobby.name}', '{lobby.settings.json()}');"""
                cursor.execute(query)
                self._conn.commit()
        except Exception as e:
            print('Exception arose:', e)
            raise

    def _add_bulk(self, lobbies: list[GameLobby]) -> None:
        pass
