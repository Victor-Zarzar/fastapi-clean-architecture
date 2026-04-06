from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.models.user import User
from app.services.user_service import get_by_username
from app.utils.utils import InvalidJWTError, decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", scheme_name="JWT")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    cred_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        sub = payload.get("sub")
        if not sub:
            raise cred_exc
    except InvalidJWTError:
        raise cred_exc

    user = get_by_username(db, sub)
    if not user:
        raise cred_exc
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def require_role(required: str):
    def _dep(current_user: User = Depends(get_current_active_user)) -> User:
        if current_user.role != required:
            raise HTTPException(status_code=403, detail="Forbidden")
        return current_user

    return _dep


AdminOnly = require_role("admin")

__all__ = [
    "oauth2_scheme",
    "get_current_user",
    "get_current_active_user",
    "require_role",
    "AdminOnly",
]
