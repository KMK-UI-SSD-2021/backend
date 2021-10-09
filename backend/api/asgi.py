import sqlite3
from typing import Callable

from fastapi import FastAPI

from backend.api.router import router
from backend.config import Config
from backend.repositories.user_repository import UserRepository


def startup_handler(application: FastAPI) -> Callable:  # pragma: no cover
    async def startup() -> None:
        application.state.db_conn = sqlite3.connect(Config().db_path)
        application.state.user_repo = UserRepository(application.state.db_conn)
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
