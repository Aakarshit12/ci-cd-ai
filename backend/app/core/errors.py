from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger("app")


async def db_exception_handler(request: Request, exc: SQLAlchemyError):
    logger.error("Database error", exc_info=exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal database error"},
    )
