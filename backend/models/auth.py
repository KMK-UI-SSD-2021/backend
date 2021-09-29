from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    username: str
    joined_at: datetime


class UserInDb(User):
    token: str
    hashed_password: str

