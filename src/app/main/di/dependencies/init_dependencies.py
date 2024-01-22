import os
from functools import partial

from fastapi import FastAPI

from app.infrastructure.database.database import (
    create_async_session_maker,
    get_async_session,
)
from app.main.di.dependencies.stub import get_session_stub


def init_dependencies(app: FastAPI):
    async_session_maker = create_async_session_maker(os.environ['db_uri'])

    app.dependency_overrides[get_session_stub] = partial(
        get_async_session,
        async_session_maker,
    )
