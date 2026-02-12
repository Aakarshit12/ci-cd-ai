from fastapi import FastAPI, Request
import time
import logging
from sqlalchemy.exc import SQLAlchemyError
from fastapi.middleware.cors import CORSMiddleware

from app.core.logging import setup_logging
from app.core.errors import db_exception_handler
from app.core.database import Base, engine

from app.models.user import User   # ✅ REQUIRED (registers model)

from app.api import requests
from app.api import ai
from app.api.auth import router as auth_router
from app.core.cache import redis_client


setup_logging()

app = FastAPI(title="AI CI/CD Backend")

app.include_router(auth_router)
app.include_router(ai.router)
app.include_router(requests.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/redis-test")
def redis_test():
    redis_client.set("test_key", "working")
    value = redis_client.get("test_key")
    return {"redis_value": value}

app.add_exception_handler(SQLAlchemyError, db_exception_handler)

logger = logging.getLogger("app")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = round(time.time() - start_time, 4)

    logger.info(
        "request completed",
        extra={
            "method": request.method,
            "path": request.url.path,
            "status": response.status_code,
            "duration": duration,
        },
    )
    return response


def init_db(max_retries: int = 10, delay_seconds: float = 2.0) -> None:
    """
    Ensure the database is reachable before serving requests.
    Retries a few times instead of crashing the container if Postgres isn't ready yet.
    """
    attempt = 0
    while attempt < max_retries:
        try:
            Base.metadata.create_all(bind=engine)
            logger.info("Database initialized successfully")
            return
        except SQLAlchemyError as exc:
            attempt += 1
            logger.warning(
                "Database initialization failed (attempt %s/%s): %s",
                attempt,
                max_retries,
                exc,
            )
            time.sleep(delay_seconds)

    logger.error("Database initialization failed after %s attempts. Exiting.", max_retries)
    raise RuntimeError("Could not initialize database")


# 🔥 MUST RUN AFTER MODEL IMPORT
init_db()


@app.get("/health")
def health():
    return {"status": "ok"}
