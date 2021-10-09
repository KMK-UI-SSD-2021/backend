from pathlib import Path

from pydantic import BaseModel


class Config(BaseModel):
    salt: str = ''  # Keep this one in secret
    db_path: str = Path('/app/backend/db.sqlite3')
