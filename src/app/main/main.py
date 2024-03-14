import logging

from fastapi import FastAPI

from app.main.di.dependencies.init_dependencies import init_dependencies
from app.main.exceptions.setup_exception_handlers import setup_exception_handlers
from app.presentators.api.root_router import root_router


logging.basicConfig(
    level=logging.INFO,
    format='{asctime} - [{levelname}] - {name} - {funcName}:{lineno} - {message}',
    style='{',
    datefmt='%Y-%m-%d %H:%M:%S',
)


def create_app() -> FastAPI:
    app = FastAPI()
    setup_exception_handlers(app)
    init_dependencies(app)
    app.include_router(root_router)
    return app


app = create_app()
