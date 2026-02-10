import logging

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from app.main.exception_handlers import setup_exception_handlers
from app.main.providers.build import build_container
from app.presentators.api.root_router import root_router

logging.basicConfig(
    level=logging.INFO,
    format='{asctime} - [{levelname}] - {funcName}:{lineno} - {message}',
    style='{',
    datefmt='%Y-%m-%d %H:%M:%S',
)


def create_app() -> FastAPI:
    app = FastAPI()
    setup_exception_handlers(app)
    container = build_container()
    setup_dishka(container=container, app=app)
    app.include_router(root_router)
    return app


app = create_app()
