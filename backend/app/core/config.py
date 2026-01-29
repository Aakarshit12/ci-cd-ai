import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:Aakarshit12@localhost:5432/ci_cd_db"
)
