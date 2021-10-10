import sqlite3
from typing import Callable

from fastapi import FastAPI, Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_401_UNAUTHORIZED

from backend.api.router import router
from backend.config import Config
from backend.repositories.lobby_repository import LobbyRepository
from backend.repositories.user_repository import UserRepository


def startup_handler(application: FastAPI) -> Callable:  # pragma: no cover
    async def startup() -> None:
        application.state.db_conn = sqlite3.connect(Config().db_path)
        application.state.user_repo = UserRepository(application.state.db_conn)
        application.state.lobby_repo = LobbyRepository(application.state.db_conn)
    return startup


def get_application() -> FastAPI:
    application = FastAPI(
        title='API',
        version='0.1',
        description='An API for the KMK project'
    )

    application.add_event_handler('startup', startup_handler(application))
    application.include_router(router, prefix='/api/v1')

    return application


app = get_application()


@app.middleware('http')
async def auth_middleware(request: Request, call_next: Callable):
    if request.url.path not in [
        '/docs',
        '/openapi.json',
        '/api/v1/register',
        '/api/v1/login'
    ]:
        repo = app.state.user_repo
        if token := request.headers.get('token'):
            if user := repo.get_user_by_token(token):
                request.scope['user'] = user

        if request.scope.get('user') is None:
            return JSONResponse(content={'error': 'unauthorized'},
                                status_code=HTTP_401_UNAUTHORIZED)

    response = await call_next(request)
    return response
