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
    EMAIL_VERIFICATION = "email_verification"


password_hash = PasswordHash.recommended()

InvalidJWTError = InvalidTokenError

EMAIL_REGEX = re.compile(
    r"([A-Za-z0-9]+[._-])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Za-z]{2,})+"
)

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS


def create_email_verification_token(
    data: dict[str, Any],
    expires_minutes: int = 30,
) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=expires_minutes)
    to_encode.update(
        {
            "exp": expire,
            "token_type": TokenType.EMAIL_VERIFICATION.value,
        }
    )
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_access_token(
    data: dict[str, Any], expires_minutes: int | None = None
) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(
        minutes=expires_minutes or ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update(
        {
            "exp": expire,
            "token_type": TokenType.ACCESS,
        }
    )
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(
    data: dict[str, Any], expires_delta: timedelta | None = None
) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + (
        expires_delta or timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )
    to_encode.update(
        {
            "exp": expire,
            "token_type": TokenType.REFRESH,
        }
    )
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return password_hash.verify(plain, hashed)


async def verify_token(
    token: str,
    expected_type: TokenType,
    redis_manager: RedisManager | None = None,
) -> dict[str, Any]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except InvalidTokenError as exc:
        raise InvalidJWTError("Invalid or expired token.") from exc

    token_type = payload.get("token_type")

    if token_type != expected_type.value:
        raise InvalidJWTError("Invalid token type.")

    if expected_type == TokenType.EMAIL_VERIFICATION.value:
        return payload

    redis_manager = redis_manager or RedisManager()

    exists = await redis_manager.check_if_jwt_exists(token)
    if not exists:
        raise InvalidJWTError("Token not found in Redis.")

    is_blacklisted = await redis_manager.is_token_blacklisted(token)
    if is_blacklisted:
        raise InvalidJWTError("Token revoked.")

    return payload


def is_email_valid(email: str) -> bool:
    return bool(re.fullmatch(EMAIL_REGEX, email))
