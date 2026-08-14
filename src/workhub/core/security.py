from datetime import datetime, timedelta, timezone
import hashlib
import secrets
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from workhub.core.config import config


password_hasher = PasswordHasher()


def hash_password(password: str) -> str:
    """Hash a plain-text password using Argon2."""
    return password_hasher.hash(password)


def verify_password(
    plain_password: str,
    password_hash: str,
) -> bool:
    """Verify a plain-text password against an Argon2 hash."""
    try:
        return password_hasher.verify(
            password_hash,
            plain_password,
        )
    except VerifyMismatchError:
        return False


def create_access_token(
    user_id: str,
    role: str,
) -> str:
    """Create a JWT access token."""

    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": user_id,
        "role": role,
        "exp": expires_at,
    }

    return jwt.encode(
        payload,
        config.JWT_SECRET_KEY,
        algorithm=config.JWT_ALGORITHM,
    )


def decode_access_token(token: str) -> dict:
    """Decode and validate a JWT access token."""

    return jwt.decode(
        token,
        config.JWT_SECRET_KEY,
        algorithms=[config.JWT_ALGORITHM],
    )

def create_refresh_token() -> str:
    """Create a secure opaque refresh token."""

    return secrets.token_urlsafe(32)


def hash_refresh_token(token: str) -> str:
    """Hash a refresh token before storing it."""

    return hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()