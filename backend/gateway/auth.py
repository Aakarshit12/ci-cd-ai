import os
from typing import Optional, Tuple

from fastapi import Request
from jose import JWTError, jwt

from app.core.config import ALGORITHM

JWT_SECRET = os.getenv(
    "JWT_SECRET", os.getenv("SECRET_KEY", "CHANGE_THIS_TO_A_LONG_RANDOM_STr")
)


def get_token_from_header(request: Request) -> Optional[str]:
    authorization = request.headers.get("Authorization")
    if not authorization:
        return None

    parts = authorization.split()
    if len(parts) == 2 and parts[0].lower() == "bearer":
        return parts[1]

    # If the user passed token without bearer
    if len(parts) == 1:
        return parts[0]

    return None


def validate_token(request: Request) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Validates JWT token on every request.
    Extracts user_id and api_key from the JWT if present.
    Returns: (is_valid, user_id, api_key)
    """
    token = get_token_from_header(request)
    if not token:
        return False, None, None

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])

        user_id = payload.get("sub")

        # User defined requirements: "extracts api key from Authorization header"
        # "validate JWT token on every request... extract user_id and api_key"
        # We try to extract api_key from the jwt payload if it exists.
        # Alternatively, if they are packing the api_key in the token string
        #  itself intentionally
        # as a non-JWT, it will throw a JWTError and fail validation.
        api_key = payload.get("api_key")

        if not user_id:
            return False, None, None

        return True, str(user_id), api_key

    except JWTError:
        return False, None, None
