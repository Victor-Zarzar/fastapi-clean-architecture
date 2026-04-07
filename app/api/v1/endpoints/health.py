from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import AdminOnly
from app.db.database import get_db
from app.models.user import User
from app.schemas.health import HealthCheckOut
from app.services.health_service import HealthService

router = APIRouter(
    prefix="/health",
    tags=["health"],
)


@router.get("", response_model=HealthCheckOut)
def health_check(
    current_user: User = Depends(AdminOnly),
    db: Session = Depends(get_db),
) -> HealthCheckOut:
    return HealthService.execute(db=db, current_user=current_user)
