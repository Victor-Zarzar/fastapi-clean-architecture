import io

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_active_user, get_db
from app.models.user import User
from app.repository.user import UserRepository
from app.schemas.two_factor import Enable2FAResponse
from app.services.two_factor_service import TwoFactorService

router = APIRouter(prefix="/2fa", tags=["2FA"])


def get_2fa_service(db: Session = Depends(get_db)) -> TwoFactorService:
    return TwoFactorService(UserRepository(db))


@router.post("/enable", response_model=Enable2FAResponse)
def enable_2fa(
    current_user: User = Depends(get_current_active_user),
    service: TwoFactorService = Depends(get_2fa_service),
):
    return service.enable_2fa(current_user)


@router.get("/qrcode")
def get_qr_code(
    current_user: User = Depends(get_current_active_user),
    service: TwoFactorService = Depends(get_2fa_service),
):
    try:
        qr_bytes = service.get_qr_code_bytes(current_user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return StreamingResponse(io.BytesIO(qr_bytes), media_type="image/png")


@router.delete("/disable")
def disable_2fa(
    current_user: User = Depends(get_current_active_user),
    service: TwoFactorService = Depends(get_2fa_service),
):
    service.disable_2fa(current_user)
    return {"detail": "2FA disabled."}
