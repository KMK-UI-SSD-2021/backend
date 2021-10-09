import sqlite3

from fastapi import APIRouter
from starlette.responses import JSONResponse
from starlette.status import (HTTP_200_OK, HTTP_201_CREATED,
                              HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND)

from backend.config import Config
from backend.models.base import GameLobby, GameSettings, Image
from backend.repositories.lobby_repository import LobbyRepository
from backend.services.auth import create_user, login_user

router = APIRouter()
connection = sqlite3.connect(Config().db_path)


@router.post('/register')
async def register(username: str, password: str):
    if token := create_user(username, password):
        return JSONResponse(content={'token': token}, status_code=HTTP_201_CREATED)

    return JSONResponse(content={'error': 'user exists'}, status_code=HTTP_400_BAD_REQUEST)


@router.post('/login')
async def login(username: str, password: str):
    if token := login_user(username, password):
        return JSONResponse(content={'token': token}, status_code=HTTP_200_OK)

    return JSONResponse(content={'error': 'wrong credentials'}, status_code=HTTP_400_BAD_REQUEST)


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

    return JSONResponse(content={'status': 'created'}, status_code=HTTP_200_OK)


@router.get('/get_lobby/{lobby_id}')
async def get_lobby(lobby_id: int):
    repo = LobbyRepository(connection)
    lobby = repo.get(lobby_id)

    if lobby is None:
        return JSONResponse(content={'error': 'Not found'}, status_code=HTTP_404_NOT_FOUND)

    return JSONResponse(content=lobby.dict())
