from fastapi import FastAPI, Request
import time
import logging
from sqlalchemy.exc import SQLAlchemyError

from app.core.logging import setup_logging
from app.core.errors import db_exception_handler
from app.api import requests
from app.core.database import Base, engine

setup_logging()

app = FastAPI(title="AI CI/CD Backend")

# register exception handler
app.add_exception_handler(SQLAlchemyError, db_exception_handler)

# request logging middleware
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

Base.metadata.create_all(bind=engine)

app.include_router(requests.router)

@app.get("/health")
def health():
    return {"status": "ok"}
