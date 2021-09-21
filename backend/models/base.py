from pydantic import BaseModel

from typing import Literal


class Image(BaseModel):
    url: str


class GameSettings(BaseModel):
    images_batch: Literal[2, 3, 4]
    images: list[Image]
    tags: list[str]


class GameLobby(BaseModel):
    owner: str = 'Admin'
    name: str
    settings: GameSettings
