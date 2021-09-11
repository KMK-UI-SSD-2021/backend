from fastapi import FastAPI


def get_application() -> FastAPI:
    application = FastAPI(
        title='MKM API',
        version='0.1',
        description='An API fro the KMK project'
    )
    return application


app = get_application()
