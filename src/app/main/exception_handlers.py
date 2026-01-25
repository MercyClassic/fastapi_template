import logging
from collections.abc import Callable
from functools import partial

from fastapi import FastAPI
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(Exception, unexpected_error_log)


def get_error_handler(
        error_info: str,
        status_code: int,
) -> Callable[[str, int], JSONResponse]:
    return partial(
        error_handler,
        error_info=error_info,
        status_code=status_code,
    )


def error_handler(
    _: Request,
    ex: Exception,
    error_info: str,
    status_code: int,
) -> JSONResponse:
    logger.error(ex, exc_info=True)
    return JSONResponse(
        status_code=status_code,
        content={'detail': error_info},
    )


async def unexpected_error_log(
        _: Request,
        ex: Exception,
) -> JSONResponse:
    logger.error(ex, exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content='Something went wrong',
    )
