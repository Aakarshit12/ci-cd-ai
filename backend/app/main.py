from fastapi import FastAPI
from app.core.database import Base, engine
from app.api import requests
from app.models import user, request  # noqa

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI CI/CD Backend")

app.include_router(requests.router)

@app.get("/health")
def health():
    return {"status": "ok"}
