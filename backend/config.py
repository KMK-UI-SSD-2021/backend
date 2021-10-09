import sqlite3
from pathlib import Path

from pydantic import BaseModel


class Config(BaseModel):
    salt: str = ''  # Keep this one in secret
    db_path: str = Path('/app/backend/db.sqlite3')


class ConfigurationManager:

    def __init__(self):
        self._config = Config()
        self.db_conn = sqlite3.connect(self._config.db_path)
