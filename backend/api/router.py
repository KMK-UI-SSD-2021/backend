from fastapi import APIRouter, Request
from starlette.responses import JSONResponse
from starlette.status import (HTTP_200_OK, HTTP_201_CREATED,
                              HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND)

from backend.models.auth import UserInRequest
from backend.models.lobby import LobbyInRequest
from backend.models.statistics import UserChoices
from backend.services import auth as auth_service
from backend.services import lobby as lobby_service
from backend.services import statistics as statistics_service

router = APIRouter()


@router.post('/register')
async def register(request: Request, user: UserInRequest):
    user_repo = request.app.state.user_repo
    if token := auth_service.create_user(user_repo, user.username, user.password):
        return JSONResponse(content={'token': token}, status_code=HTTP_201_CREATED)

    return JSONResponse(content={'error': 'user exists'}, status_code=HTTP_400_BAD_REQUEST)


@router.post('/login')
async def login(request: Request, user: UserInRequest):
    user_repo = request.app.state.user_repo
    if token := auth_service.login_user(user_repo, user.username, user.password):
        return JSONResponse(content={'token': token}, status_code=HTTP_200_OK)

    return JSONResponse(content={'error': 'wrong credentials'}, status_code=HTTP_400_BAD_REQUEST)


@router.post('/lobby')
async def create_lobby(request: Request, lobby_in_request: LobbyInRequest):
    lobby_repo = request.app.state.lobby_repo
    statistics_repo = request.app.state.statistics_repo

    lobby_id = lobby_service.create_lobby(request.user,
                                          statistics_repo,
                                          lobby_repo,
                                          lobby_in_request)

    return JSONResponse(content={'lobby_id': lobby_id}, status_code=HTTP_201_CREATED)


@router.get('/lobby/{lobby_id}')
async def get_lobby(request: Request, lobby_id: int):
    lobby_repo = request.app.state.lobby_repo

    lobby = lobby_service.get_lobby(request.user, lobby_repo, lobby_id)
    if lobby is None:
        return JSONResponse(content={'error': 'not found'}, status_code=HTTP_404_NOT_FOUND)

    return JSONResponse(content=lobby.dict(), status_code=HTTP_200_OK)


@router.put('/statistics/{lobby_id}')
async def submit_choices(request: Request, choices: UserChoices, lobby_id: str):
    lobby_repo = request.app.state.lobby_repo
    statistics_repo = request.app.state.statistics_repo

    statistics = statistics_service.get_statistics(request.user, statistics_repo,
                                                   lobby_repo, lobby_id)
    if statistics is None:
        return JSONResponse(content={'error': 'not found'}, status_code=HTTP_404_NOT_FOUND)

    updated_statistics = statistics_service.update_statistics(statistics_repo, statistics,
                                                              choices)
    return JSONResponse(content=updated_statistics.dict(), status_code=HTTP_200_OK)


@router.get('/statistics/{lobby_id}')
async def get_statistics(request: Request, lobby_id: int):
    lobby_repo = request.app.state.lobby_repo
    statistics_repo = request.app.state.statistics_repo

    statistics = statistics_service.get_statistics(request.user, statistics_repo,
                                                   lobby_repo, lobby_id)
    if statistics is None:
        return JSONResponse(content={'error': 'not found'}, status_code=HTTP_404_NOT_FOUND)

    return JSONResponse(content=statistics.dict(), status_code=HTTP_200_OK)
