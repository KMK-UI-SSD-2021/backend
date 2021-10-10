from typing import Literal

from pydantic import BaseModel


class Image(BaseModel):
    url: str


class Settings(BaseModel):
    images_batch: Literal[2, 3, 4]
    images: list[Image]
    tags: list[str]


class Lobby(BaseModel):
    owner: str
    name: str
    settings: Settings


class LobbyInRequest(BaseModel):
    name: str
    settings: Settings
