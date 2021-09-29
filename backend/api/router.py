import sqlite3
import secrets
from datetime import datetime

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.responses import JSONResponse
from starlette.status import (HTTP_200_OK, HTTP_201_CREATED,
                              HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND)

from backend.config import Config
from backend.auth.utils import check_password, hash_password
from backend.models.auth import UserInDb
from backend.models.base import Image, GameSettings, GameLobby
from backend.repositories.lobby_repository import LobbyRepository
from backend.repositories.user_repository import UserRepository

router = APIRouter()
connection = sqlite3.connect(Config().db_path)


@router.post('/register')
async def register(username: str, password: str):
    repo = UserRepository(connection)

    joined_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    hashed_password = hash_password(password)
    token = secrets.token_hex()

    exists = bool(repo.get_hashed_password(username))
    if exists:
        return JSONResponse(content={'error': 'user exists'}, status_code=HTTP_400_BAD_REQUEST)

    user_in_db = UserInDb(username=username,
                          joined_at=joined_at,
                          hashed_password=hashed_password,
                          token=token)

    repo._add(user_in_db)
    return JSONResponse(content={'token': token}, status_code=HTTP_201_CREATED)


@router.post('/login')
async def login(username: str, password: str):
    repo = UserRepository(connection)

    expected_hashed_password = repo.get_hashed_password(username)
    if check_password(password, expected_hashed_password):
        token = repo.get_token(username)
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

    return JSONResponse(content=lobby.json())

