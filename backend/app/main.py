import logging
import os
import sys
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy.exc import SQLAlchemyError

from app.api import ai, requests
from app.api.auth import router as auth_router
from app.core import cache
from app.core.database import Base, engine
from app.core.errors import db_exception_handler
from app.core.logging import setup_logging
from gateway.middleware import GatewayMiddleware

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

setup_logging()

app = FastAPI(title="AI CI/CD Backend")

# Instrument the app to expose default Prometheus metrics
Instrumentator().instrument(app).expose(app)

from app.api import ai, requests
from app.api.auth import router as auth_router
from gateway.router import router as gateway_router

app.include_router(auth_router)
app.include_router(ai.router)
app.include_router(requests.router)
app.include_router(gateway_router, prefix="/gateway/services", tags=["gateway"])

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

app.add_middleware(GatewayMiddleware)


@app.get("/redis-test")
def redis_test():
    cache.redis_client.set("test_key", "working")
    value = cache.redis_client.get("test_key")
    return {"redis_value": value}


app.add_exception_handler(SQLAlchemyError, db_exception_handler)

logger = logging.getLogger("app")


def is_testing() -> bool:
    """
    Centralised check for test mode so that env handling
    is consistent across local runs and CI.
    """
    return os.getenv("TESTING", "").lower() in {"1", "true", "yes"}


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

    logger.error(
        "Database initialization failed after %s attempts. Exiting.", max_retries
    )
    raise RuntimeError("Could not initialize database")


# 🔥 MUST RUN AFTER MODEL IMPORT


from gateway.health_check import start_health_check_task

@app.on_event("startup")
def startup_event():
    # Avoid touching the real database during unit tests
    # (both locally and in CI) – integration tests can
    # run with TESTING unset/false to exercise init_db().
    if not is_testing():
        init_db()
        start_health_check_task()


@app.get("/health")
def health():
    return {"status": "ok"}
