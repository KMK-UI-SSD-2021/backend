import json
from contextlib import closing
from sqlite3 import Connection
from typing import Optional

from backend.models.statistics import Statistics
from backend.repositories.abstract import AbstractRepository


class StatisticsRepository(AbstractRepository):

    def __init__(self, conn: Connection) -> None:
        self._conn = conn
        self._init_db()

    def _init_db(self) -> None:
        try:
            with closing(self._conn.cursor()) as cursor:
                query = """CREATE TABLE IF NOT EXISTS statistics
                           (id INTEGER PRIMARY KEY,
                            lobby_id INTEGER NOT NULL UNIQUE,
                            times_gathered INTEGER,
                            image_tags_counts VARCHAR (4096));"""
                cursor.execute(query)
                self._conn.commit()

        except Exception as e:  # pragma: no cover
            print('Exception arose:', e)
            raise

    def _add(self, statistics: Statistics) -> None:
        try:
            with closing(self._conn.cursor()) as cursor:
                query = """INSERT INTO statistics (lobby_id, times_gathered, image_tags_counts)
                           VALUES (?, ?, ?);"""
                cursor.execute(query, (statistics.lobby_id,
                                       statistics.times_gathered,
                                       json.dumps(statistics.image_tags_counts)))
                self._conn.commit()

        except Exception as e:  # pragma: no cover
            print('Exception arose:', e)
            raise

    def get(self, lobby_id: int) -> Optional[Statistics]:
        try:
            with closing(self._conn.cursor()) as cursor:
                query = """SELECT times_gathered, image_tags_counts FROM statistics
                           WHERE lobby_id = ?;"""
                cursor.execute(query, (lobby_id, ))

                if data := cursor.fetchone():
                    return Statistics(lobby_id=lobby_id,
                                      times_gathered=data[0],
                                      image_tags_counts=json.loads(data[1]))

        except Exception as e:  # pragma: no cover
            print('Exception arose:', e)
            raise

    def update(self, statistics: Statistics) -> None:
        try:
            with closing(self._conn.cursor()) as cursor:
                query = """UPDATE statistics
                           SET times_gathered = ?, image_tags_counts = ?
                           WHERE lobby_id = ?;"""
                cursor.execute(query, (statistics.times_gathered,
                                       json.dumps(statistics.image_tags_counts),
                                       statistics.lobby_id))
                self._conn.commit()

        except Exception as e:  # pragma: no cover
            print('Exception arose:', e)
            raise

    def _add_bulk(self) -> None:  # pragma: no cover
        pass
