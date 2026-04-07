from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> User | None:
        stmt = select(User).where(User.id == user_id)
        result = self.db.execute(stmt)
        return result.scalar_one_or_none()

    def get_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        result = self.db.execute(stmt)
        return result.scalar_one_or_none()

    def create(
        self,
        *,
        username: str,
        hashed_password: str,
        full_name: str | None = None,
        email: str | None = None,
        role: str = "basic",
        disabled: bool = False,
    ) -> User:
        user = User(
            username=username,
            hashed_password=hashed_password,
            full_name=full_name,
            email=email,
            role=role,
            disabled=disabled,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
