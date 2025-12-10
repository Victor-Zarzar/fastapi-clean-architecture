from typing import Optional

from sqlalchemy.orm import Session

from app.models.user import User
from app.utils.utils import hash_password, verify_password


def get_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()


def create_user(
    db: Session,
    *,
    username: str,
    password: str,
    full_name: str | None = None,
    email: str | None = None,
    role: str = "basic",
    disabled: bool = False,
) -> User:
    obj = User(
        username=username,
        full_name=full_name,
        email=email,
        role=role,
        disabled=disabled,
        hashed_password=hash_password(password),
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def authenticate(db: Session, username: str, password: str) -> Optional[User]:
    user = get_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def ensure_admin(
    db: Session,
    *,
    username: str,
    password: str,
    full_name: str,
    email: str,
    disabled: bool,
) -> User:
    admin = get_by_username(db, username)
    if admin:
        return admin
    return create_user(
        db,
        username=username,
        password=password,
        full_name=full_name,
        email=email,
        role="admin",
        disabled=disabled,
    )
