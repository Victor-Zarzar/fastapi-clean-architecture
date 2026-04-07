from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserOut
from app.services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["user"],
)


@router.get("/me", response_model=UserOut)
def read_users_me(
    current_user: User = Depends(get_current_user),
):
    return current_user


@router.get("", response_model=list[UserOut])
def read_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = UserService(db)
    users = service.get_all()
    return users


@router.get("/{user_id}", response_model=UserOut)
def read_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = UserService(db)
    user = service.get_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    return user
