from sqlalchemy.orm import Session

from app.models.user import User
from app.repository.user import UserRepository
from app.utils.utils import hash_password, verify_password


class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def get_by_id(self, user_id: int) -> User | None:
        return self.repository.get_by_id(user_id)

    def get_by_username(self, username: str) -> User | None:
        return self.repository.get_by_username(username)

    def create_user(
        self,
        *,
        username: str,
        password: str,
        full_name: str | None = None,
        email: str | None = None,
        role: str = "basic",
        disabled: bool = False,
    ) -> User:
        hashed_password = hash_password(password)
        return self.repository.create(
            username=username,
            hashed_password=hashed_password,
            full_name=full_name,
            email=email,
            role=role,
            disabled=disabled,
        )

    def authenticate(self, username: str, password: str) -> User | None:
        user = self.repository.get_by_username(username)
        if not user or not verify_password(password, user.hashed_password):
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
    ) -> User:
        admin = self.repository.get_by_username(username)
        if admin:
            return admin
        return self.create_user(
            username=username,
            password=password,
            full_name=full_name,
            email=email,
            role="admin",
            disabled=disabled,
        )
