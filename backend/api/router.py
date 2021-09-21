import sqlite3

from fastapi import APIRouter
from starlette.responses import JSONResponse

from backend.config import Config
from backend.models.base import Image, GameSettings, GameLobby
from backend.repositories.lobby_repository import LobbyRepository

router = APIRouter()
connection = sqlite3.connect(Config().db_path)


@router.get('/create_lobby')
async def create_lobby():
    images = [
        Image(url='https://imgur.com/sKV54PO'),
        Image(url='https://imgur.com/sKV54PO'),
        Image(url='https://imgur.com/sKV54PO'),
    ]
    tags = ['Like', 'Dislike']
    settings = GameSettings(images_batch=3, images=images, tags=tags)
    lobby = GameLobby(name='Test game lobby', settings=settings)

    repo = LobbyRepository(connection)
    repo._add(lobby)

    return 200


@router.get('/get_lobby/{lobby_id}')
async def get_lobby(lobby_id: int):
    repo = LobbyRepository(connection)
    lobby = repo.get(lobby_id)

    if lobby is None:
        return JSONResponse(content={'error': 'Not found'}, status_code=404)

    return JSONResponse(content=lobby.json())

