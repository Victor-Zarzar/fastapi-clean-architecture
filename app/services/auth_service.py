from jwt import InvalidTokenError

from app.core.execeptions import AuthError
from app.helpers.redis import RedisManager
from app.repository.user import UserRepository
from app.utils.utils import (
    TokenType,
    create_access_token,
    create_refresh_token,
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
