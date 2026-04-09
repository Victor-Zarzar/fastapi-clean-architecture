from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from jwt import InvalidTokenError
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_active_user
from app.core.execeptions import AuthError
from app.core.redis import get_redis
from app.db.database import get_db
from app.helpers.redis import RedisManager
from app.models.user import User
from app.repository.user import UserRepository
from app.schemas.auth import (
    ChangePasswordRequest,
    ForgotPasswordRequest,
    ResendVerificationRequest,
    ResetPasswordRequest,
    Token,
    VerifyEmailRequest,
)
from app.schemas.user import UserCreate, UserOut
from app.services.auth_service import AuthService
from app.services.email_service import EmailDeliveryError, EmailService
from app.services.user_service import (
    InvalidEmailVerificationError,
    UserAlreadyExistsError,
    UserService,
)
from app.utils.utils import TokenType, decode_token, verify_token

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
async def sign_up(
    payload: UserCreate,
    user_service: UserService = Depends(get_user_service),
    redis: RedisManager = Depends(get_redis),
) -> UserOut:
    try:
        user = user_service.create_user(
            username=payload.username,
            password=payload.password,
            full_name=payload.full_name,
            email=payload.email,
        )

        token = user_service.generate_email_verification_token(user)
        token_payload = decode_token(token)

        await redis.put_jwt_redis(token, token_payload["exp"])

        EmailService().send_email_verification(
            to_email=user.email,
            username=user.username,
            token=token,
        )

        return UserOut.model_validate(user)

    except UserAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc
    except EmailDeliveryError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
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
        result = await auth_service.refresh_access_token(refresh_token, redis)

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


@router.post("/verify-email", status_code=status.HTTP_200_OK)
async def verify_email(
    payload: VerifyEmailRequest,
    user_service: UserService = Depends(get_user_service),
    redis: RedisManager = Depends(get_redis),
):
    try:
        token_exists = await redis.check_if_jwt_exists(payload.token)
        if not token_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Verification token is invalid, expired, or already used.",
            )

        decoded = await verify_token(
            token=payload.token,
            expected_type=TokenType.EMAIL_VERIFICATION,
        )

        user = user_service.verify_user_email(decoded)

        token_payload = decode_token(payload.token)
        await redis.blacklist_token(payload.token, token_payload["exp"])

        return {
            "message": "Email verified successfully.",
            "email": user.email,
            "email_verified": user.email_verified,
        }

    except InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except InvalidEmailVerificationError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.post("/resend-verification-email", status_code=status.HTTP_200_OK)
async def resend_verification_email(
    payload: ResendVerificationRequest,
    user_service: UserService = Depends(get_user_service),
    redis: RedisManager = Depends(get_redis),
):
    user = user_service.get_by_email(payload.email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    if user.email_verified:
        return {"message": "Email already verified."}

    token = user_service.generate_email_verification_token(user)
    token_payload = decode_token(token)

    await redis.put_jwt_redis(token, token_payload["exp"])

    EmailService().send_email_verification(
        to_email=user.email,
        username=user.username,
        token=token,
    )

    return {"message": "Verification email sent successfully."}


@router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password(
    payload: ForgotPasswordRequest,
    auth_service: AuthService = Depends(get_auth_service),
    redis: RedisManager = Depends(get_redis),
):
    user = auth_service.user_repository.get_by_email(payload.email)

    if not user:
        return {"message": "If the email exists, a password reset link has been sent."}

    if user.disabled:
        return {"message": "If the email exists, a password reset link has been sent."}

    token = auth_service.generate_password_reset_token(user)
    token_payload = decode_token(token)

    await redis.put_jwt_redis(token, token_payload["exp"])

    EmailService().send_password_reset_email(
        to_email=user.email,
        username=user.username,
        token=token,
    )

    return {"message": "If the email exists, a password reset link has been sent."}


@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(
    payload: ResetPasswordRequest,
    auth_service: AuthService = Depends(get_auth_service),
    redis: RedisManager = Depends(get_redis),
):
    try:
        await auth_service.reset_password(
            token=payload.token,
            new_password=payload.new_password,
            redis_manager=redis,
        )

        return {"message": "Password reset successfully."}

    except AuthError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.post("/change-password", status_code=status.HTTP_200_OK)
async def change_password(
    payload: ChangePasswordRequest,
    current_user: User = Depends(get_current_active_user),
    auth_service: AuthService = Depends(get_auth_service),
):
    try:
        auth_service.change_password(
            user=current_user,
            current_password=payload.current_password,
            new_password=payload.new_password,
        )

        return {"message": "Password updated successfully."}

    except AuthError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
