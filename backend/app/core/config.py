import os
from datetime import timedelta

SECRET_KEY = "CHANGE_THIS_TO_A_LONG_RANDOM_STr"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:Aakarshit12@localhost:5432/ci_cd_db"
)
