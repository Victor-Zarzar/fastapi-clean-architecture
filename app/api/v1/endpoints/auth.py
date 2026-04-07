from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.execeptions import AuthError
from app.db.database import get_db
from app.repository.user import UserRepository
from app.schemas.auth import Token
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    user_repository = UserRepository(db)
    return AuthService(user_repository)


@router.post("/signin", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthService = Depends(get_auth_service),
) -> Token:
    try:
        result = auth_service.sign_in(
            username=form_data.username,
            password=form_data.password,
        )
        return Token(**result)
    except AuthError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=exc.message,
        ) from exc


@router.post("/refresh", response_model=Token)
def refresh_access_token(
    request: Request,
    auth_service: AuthService = Depends(get_auth_service),
) -> Token:
    try:
        refresh_token = request.cookies.get("refresh_token")
        result = auth_service.refresh_access_token(refresh_token)
        return Token(**result)
    except AuthError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=exc.message,
        ) from exc
