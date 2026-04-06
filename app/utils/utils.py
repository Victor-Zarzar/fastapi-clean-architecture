import re
from datetime import UTC, datetime, timedelta
from enum import Enum
from typing import Any

import jwt
from jwt import InvalidTokenError
from pwdlib import PasswordHash

from app.core.config import settings
from app.helpers.redis import RedisManager


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


password_hash = PasswordHash.recommended()

InvalidJWTError = InvalidTokenError

EMAIL_REGEX = re.compile(
    r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
)

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS


async def create_access_token(
    data: dict[str, Any], expires_minutes: int | None = None
) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(
        minutes=expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


async def create_refresh_token(
    data: dict[str, Any], expires_delta: timedelta | None = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC).replace(tzinfo=None) + expires_delta
    else:
        expire = datetime.now(UTC).replace(tzinfo=None) + timedelta(
            days=REFRESH_TOKEN_EXPIRE_DAYS
        )
    to_encode.update({"exp": expire, "token_type": TokenType.REFRESH})
    encoded_jwt: str = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def decode_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])


def hash_password(plain: str) -> str:
    return password_hash.hash(plain)


def get_password_hash(password):
    return password_hash.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return password_hash.verify(plain, hashed)


async def verify_token(
    token: str,
    expected_type: TokenType,
    redis_manager: RedisManager | None = None,
) -> dict[str, Any]:
    redis_manager = redis_manager or RedisManager()

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except InvalidTokenError as exc:
        raise InvalidJWTError("Invalid or expired token.") from exc

    token_type = payload.get("token_type")

    if token_type is None:
        token_type = TokenType.ACCESS

    if token_type != expected_type:
        raise InvalidJWTError("Invalid token type.")

    exists = await redis_manager.check_if_jwt_exists(token)
    if not exists:
        raise InvalidJWTError("Token not found in Redis or revoked.")

    return payload


def is_email_valid(email: str) -> bool:
    if not re.fullmatch(EMAIL_REGEX, email):
        return False

    domain = email.split("@")[1]
    if domain == "gmail.com":
        return True

    return False
