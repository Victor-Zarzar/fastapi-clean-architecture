from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.redis import get_redis
from app.db.database import get_db
from app.helpers.redis import RedisManager
from app.models.user import User
from app.repository.cost import CostRepository
from app.services.cost_service import CostService
from app.services.user_service import UserService
from app.utils.utils import InvalidJWTError, decode_token

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/signin",
    scheme_name="JWT",
    auto_error=False,
)


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)


def get_cost_service(db: Session = Depends(get_db)) -> CostService:
    repository = CostRepository(db)
    return CostService(repository)


async def get_current_user(
    request: Request,
    token: str | None = Depends(oauth2_scheme),
    user_service: UserService = Depends(get_user_service),
    redis: RedisManager = Depends(get_redis),
) -> User:
    cred_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    access_token = token or request.cookies.get("access_token")
    if not access_token:
        raise cred_exc

    if not await redis.check_if_jwt_exists(access_token):
        raise cred_exc

    if await redis.is_token_blacklisted(access_token):
        raise cred_exc

    try:
        payload = decode_token(access_token)
        sub = payload.get("sub")
        if not sub:
            raise cred_exc
    except InvalidJWTError as exc:
        raise cred_exc from exc

    user = user_service.get_by_email(sub)
    if not user:
        raise cred_exc

    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
        )
    return current_user


def require_role(required: str):
    def _dep(current_user: User = Depends(get_current_active_user)) -> User:
        if current_user.role != required:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden",
            )
        return current_user

    return _dep


AdminOnly = require_role("admin")

__all__ = [
    "oauth2_scheme",
    "get_user_service",
    "get_cost_service",
    "get_current_user",
    "get_current_active_user",
    "require_role",
    "AdminOnly",
]
