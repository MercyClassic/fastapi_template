import json
import logging
import os
from functools import partial
from logging import config
from pathlib import Path

from fastapi import FastAPI
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.main.config.logging import get_logging_dict

root_dir = '%s' % Path(__file__).parent.parent.parent

if not os.path.exists(f'{root_dir}/logs/'):
    os.mkdir(f'{root_dir}/logs/')

config.dictConfig(get_logging_dict(root_dir))
logger = logging.getLogger(__name__)


def setup_exception_handlers(app: FastAPI):
    app.add_exception_handler(Exception, unexpected_error_log)


def get_error_handler(error_info: str, status_code: int):
    return partial(
        error_handler,
        error_info=error_info,
        status_code=status_code,
    )


def error_handler(
    request: Request,
    ex: Exception,
    error_info: str,
    status_code: int,
) -> JSONResponse:
    logger.error(ex, exc_info=True)
    return JSONResponse(
        status_code=status_code,
        content=json.dumps({'detail': error_info}),
    )


async def unexpected_error_log(request: Request, ex: Exception) -> JSONResponse:
    logger.error(ex, exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content='Something went wrong',
    )
