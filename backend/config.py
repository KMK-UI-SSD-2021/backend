from pathlib import Path

from pydantic import BaseModel


class Config(BaseModel):
    db_path: str = Path('/app/backend/db.sqlite3')
