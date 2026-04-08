from sqlalchemy.orm import Session

from app.models.user import User
from app.repository.user import UserRepository
from app.utils.utils import (
    create_email_verification_token,
    hash_password,
    verify_password,
)


class InvalidEmailVerificationError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class UserAlreadyExistsError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def get_by_id(self, user_id: int) -> User | None:
        return self.repository.get_by_id(user_id)

    def get_by_username(self, username: str) -> User | None:
        return self.repository.get_by_username(username)

    def get_by_email(self, email: str) -> User | None:
        return self.repository.get_by_email(email)

    def get_all(self) -> list[User]:
        return self.repository.get_all()

    def validate_email(self, email: str) -> bool:
        user = self.repository.get_by_email(email)
        return user is not None

    def create_user(
        self,
        *,
        username: str,
        password: str,
        full_name: str | None = None,
        email: str,
        role: str = "basic",
        disabled: bool = False,
        email_verified: bool = False,
    ) -> User:
        if self.repository.get_by_username(username):
            raise UserAlreadyExistsError("Username already registered.")

        if self.repository.get_by_email(email):
            raise UserAlreadyExistsError("Email already registered.")

        hashed_password = hash_password(password)

        return self.repository.create(
            username=username,
            hashed_password=hashed_password,
            full_name=full_name,
            email=email,
            role=role,
            disabled=disabled,
            email_verified=email_verified,
        )

    def authenticate_by_email(self, email: str, password: str) -> User | None:
        user = self.repository.get_by_email(email)
        if not user:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        return user

    def ensure_admin(
        self,
        *,
        username: str,
        password: str,
        full_name: str,
        email: str,
        disabled: bool,
        email_verified: bool = False,
    ) -> User:
        admin = self.repository.get_by_email(email)
        if admin:
            return admin

        return self.create_user(
            username=username,
            password=password,
            full_name=full_name,
            email=email,
            role="admin",
            disabled=disabled,
            email_verified=email_verified,
        )

    def generate_email_verification_token(self, user: User) -> str:
        return create_email_verification_token(
            {
                "sub": user.email,
                "user_id": user.id,
            }
        )

    def verify_user_email(self, token_payload: dict) -> User:
        email = token_payload.get("sub")

        if not email:
            raise InvalidEmailVerificationError("Invalid token payload.")

        user = self.repository.get_by_email(email)
        if not user:
            raise InvalidEmailVerificationError("User not found.")

        if user.email_verified:
            return user

        return self.repository.mark_email_as_verified(user)
