from jwt import InvalidTokenError
from pyotp import TOTP

from app.core.execeptions import AuthError
from app.helpers.redis import RedisManager
from app.models.user import User
from app.repository.user import UserRepository
from app.utils.utils import (
    TokenType,
    create_access_token,
    create_mfa_pending_token,
    create_password_reset_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
    verify_token,
)


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def sign_in(self, email: str, password: str) -> dict[str, str]:
        user = self.user_repository.get_by_email(email)

        if not user or not verify_password(password, user.hashed_password):
            raise AuthError("Incorrect email or password")

        if user.disabled:
            raise AuthError("User is disabled")

        if not user.email_verified:
            raise AuthError("Email not verified")

        if user.totp_enabled:
            mfa_pending_token = create_mfa_pending_token({"sub": user.email})
            return {
                "mfa_pending_token": mfa_pending_token,
                "token_type": "mfa_pending",
            }

        access_token = create_access_token({"sub": user.email, "role": user.role})
        refresh_token = create_refresh_token({"sub": user.email, "role": user.role})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "email_verified": user.email_verified,
        }

    async def verify_mfa(
        self,
        mfa_pending_token: str,
        totp_code: str,
        redis_manager: RedisManager,
    ) -> dict:
        try:
            payload = await verify_token(
                mfa_pending_token,
                TokenType.MFA_PENDING,
                redis_manager,
            )
        except InvalidTokenError as exc:
            raise AuthError("Invalid or expired MFA token.") from exc

        email = payload.get("sub")
        if not email:
            raise AuthError("Invalid token payload.")

        user = self.user_repository.get_by_email(email)
        if not user:
            raise AuthError("User not found.")

        if not TOTP(user.totp_secret).verify(totp_code):
            raise AuthError("Invalid TOTP code.")

        access_token = create_access_token({"sub": user.email, "role": user.role})
        refresh_token = create_refresh_token({"sub": user.email, "role": user.role})
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    async def refresh_access_token(
        self,
        refresh_token: str,
        redis_manager: RedisManager,
    ) -> dict[str, str]:
        if not refresh_token:
            raise AuthError("Refresh token missing.")

        try:
            payload = await verify_token(
                refresh_token, TokenType.REFRESH, redis_manager
            )
        except InvalidTokenError as exc:
            raise AuthError("Invalid refresh token.") from exc

        subject = payload.get("sub")
        role = payload.get("role")

        if not subject:
            raise AuthError("Invalid token payload.")

        access_token = create_access_token({"sub": subject, "role": role})
        refresh_token = create_refresh_token({"sub": subject, "role": role})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    def generate_password_reset_token(self, user: User) -> str:
        return create_password_reset_token(
            {
                "sub": user.email,
                "user_id": user.id,
            }
        )

    async def reset_password(
        self,
        token: str,
        new_password: str,
        redis_manager: RedisManager,
    ) -> None:
        try:
            payload = await verify_token(
                token=token,
                expected_type=TokenType.PASSWORD_RESET,
                redis_manager=redis_manager,
            )
        except InvalidTokenError as exc:
            raise AuthError("Invalid or expired reset token.") from exc

        email = payload.get("sub")
        user_id = payload.get("user_id")

        if not email or not user_id:
            raise AuthError("Invalid token payload.")

        user = self.user_repository.get_by_email(email)

        if not user or user.id != user_id:
            raise AuthError("User not found.")

        hashed_password = hash_password(new_password)
        self.user_repository.update_password(user, hashed_password)

        token_payload = decode_token(token)
        await redis_manager.blacklist_token(token, token_payload["exp"])

    def change_password(
        self,
        user: User,
        current_password: str,
        new_password: str,
    ) -> None:
        if not verify_password(current_password, user.hashed_password):
            raise AuthError("Current password is incorrect.")

        hashed_password = hash_password(new_password)
        self.user_repository.update_password(user, hashed_password)
