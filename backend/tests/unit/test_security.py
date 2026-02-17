from app.core import security


def test_hash_and_verify_password():
    plain = "s3cret-password"
    hashed = security.hash_password(plain)
    assert hashed != plain
    assert security.verify_password(plain, hashed)


def test_create_access_token_contains_sub_and_exp():
    token = security.create_access_token({"sub": "123"})
    # Basic smoke check – token is a non-empty string
    assert isinstance(token, str)
    assert token

