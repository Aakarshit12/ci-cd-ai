from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core import deps, security
from app.models.user import User


def _create_user(
    db: Session, email: str = "user@example.com", password: str = "password"
):
    user = User(email=email, hashed_password=security.hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def test_get_current_user_happy_path(db: Session):
    user = _create_user(db)
    token = security.create_access_token({"sub": str(user.id)})

    current_user = deps.get_current_user(token=token, db=db)
    assert current_user.id == user.id
    assert current_user.email == user.email


def test_get_current_user_invalid_token_raises(db: Session):
    invalid_token = "not-a-valid-jwt"

    try:
        deps.get_current_user(token=invalid_token, db=db)
    except HTTPException as exc:
        assert exc.status_code == 401
    else:
        assert False, "Expected HTTPException for invalid token"
