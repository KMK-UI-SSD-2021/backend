from fastapi import FastAPI


def get_application() -> FastAPI:
    application = FastAPI(
        title='API',
        version='0.1',
        description='An API for the KMK project'
    )
    return application


app = get_application()
