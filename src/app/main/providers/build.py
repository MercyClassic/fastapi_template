from dishka import AsyncContainer, make_async_container

from app.main.providers.db import DbProvider


def build_container() -> AsyncContainer:
    return make_async_container(DbProvider())
