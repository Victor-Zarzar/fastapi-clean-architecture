from fastapi import APIRouter, Depends

from app.core.dependencies import AdminOnly
from app.models.user import User

router = APIRouter()


@router.get("/admin")
async def whoami_admin(current_user: User = Depends(AdminOnly)):
    return {
        "username": current_user.username,
        "role": current_user.role,
        "disabled": current_user.disabled,
    }
