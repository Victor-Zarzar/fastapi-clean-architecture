from datetime import UTC, datetime

from sqlalchemy import or_, select
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

    def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        result = self.db.execute(stmt)
        return result.scalar_one_or_none()

    def get_by_username_or_email(self, username: str, email: str) -> User | None:
        stmt = select(User).where(or_(User.username == username, User.email == email))
        result = self.db.execute(stmt)
        return result.scalar_one_or_none()

    def get_all(self) -> list[User]:
        stmt = select(User)
        result = self.db.execute(stmt)
        return result.scalars().all()

    def mark_email_as_verified(self, user: User) -> User:
        user.email_verified = True
        user.email_verified_at = datetime.now(UTC)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_password(self, user: User, hashed_password: str) -> User:
        user.hashed_password = hashed_password
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def create(
        self,
        *,
        username: str,
        hashed_password: str,
        full_name: str | None = None,
        email: str | None = None,
        role: str = "basic",
        disabled: bool = False,
        email_verified: bool = False,
    ) -> User:
        user = User(
            username=username,
            hashed_password=hashed_password,
            full_name=full_name,
            email=email,
            role=role,
            disabled=disabled,
            email_verified=email_verified,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
