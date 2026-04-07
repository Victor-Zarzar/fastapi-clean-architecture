from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_active_user
from app.core.execeptions import AuthError
from app.core.redis import get_redis
from app.db.database import get_db
from app.helpers.redis import RedisManager
from app.models.user import User
from app.repository.user import UserRepository
from app.schemas.auth import Token
from app.schemas.user import UserCreate, UserOut
from app.services.auth_service import AuthService
from app.services.user_service import UserAlreadyExistsError, UserService
from app.utils.utils import decode_token

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    user_repository = UserRepository(db)
    return AuthService(user_repository)


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)


@router.post("/signup", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def sign_up(
    payload: UserCreate,
    user_service: UserService = Depends(get_user_service),
) -> UserOut:
    try:
        user = user_service.create_user(
            username=payload.username,
            password=payload.password,
            full_name=payload.full_name,
            email=payload.email,
        )
        return UserOut.model_validate(user)
    except UserAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.post("/signin", response_model=Token)
async def login_for_access_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
    redis: RedisManager = Depends(get_redis),
) -> Token:
    try:
        result = auth_service.sign_in(
            email=form_data.username,
            password=form_data.password,
        )

        access_payload = decode_token(result["access_token"])
        refresh_payload = decode_token(result["refresh_token"])

        await redis.put_jwt_redis(result["access_token"], access_payload["exp"])
        await redis.put_jwt_redis(result["refresh_token"], refresh_payload["exp"])

        response.set_cookie(
            key="access_token",
            value=result["access_token"],
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=60 * 15,
            path="/",
        )
        response.set_cookie(
            key="refresh_token",
            value=result["refresh_token"],
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=60 * 60 * 24 * 7,
            path="/api/v1/auth",
        )

        return Token(**result)

    except AuthError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc


@router.post("/signout", status_code=status.HTTP_200_OK)
async def logout(
    request: Request,
    response: Response,
    current_user: User = Depends(get_current_active_user),
    redis: RedisManager = Depends(get_redis),
):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")

    if access_token:
        try:
            payload = decode_token(access_token)
            await redis.blacklist_token(access_token, payload["exp"])
        except Exception:
            pass

    if refresh_token:
        try:
            payload = decode_token(refresh_token)
            await redis.blacklist_token(refresh_token, payload["exp"])
        except Exception:
            pass

    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/api/v1/auth")

    return {"message": f"User {current_user.email} logged out successfully"}


@router.post("/refresh", response_model=Token)
async def refresh_access_token(
    request: Request,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service),
    redis: RedisManager = Depends(get_redis),
) -> Token:
    try:
        refresh_token = request.cookies.get("refresh_token")
        result = auth_service.refresh_access_token(refresh_token)

        access_payload = decode_token(result["access_token"])
        refresh_payload = decode_token(result["refresh_token"])

        await redis.put_jwt_redis(result["access_token"], access_payload["exp"])
        await redis.put_jwt_redis(result["refresh_token"], refresh_payload["exp"])

        response.set_cookie(
            key="access_token",
            value=result["access_token"],
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=60 * 15,
            path="/",
        )
        response.set_cookie(
            key="refresh_token",
            value=result["refresh_token"],
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=60 * 60 * 24 * 7,
            path="/api/v1/auth",
        )

        return Token(**result)

    except AuthError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc
