from fastapi import FastAPI

from backend.api.router import router


def get_application() -> FastAPI:
    application = FastAPI(
        title='API',
        version='0.1',
        description='An API for the KMK project'
    )
    application.include_router(router, prefix='/api/v1')
    return application


app = get_application()
