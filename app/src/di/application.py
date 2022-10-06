from fastapi import FastAPI

from src.di.containers import Container
from src.endpoints.manager import manager_router


def create_app() -> FastAPI:
    container = Container()

    # db = container.db()
    # db.create_database()

    app = FastAPI()
    app.container = container
    app.include_router(manager_router, prefix='/api/v1/manager', tags=["Game manager"])

    return app
