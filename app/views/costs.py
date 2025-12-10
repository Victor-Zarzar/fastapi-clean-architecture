from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import AdminOnly, get_current_active_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.costs import CostOfLiving, CostOfLivingCreate
from app.services.cost_service import (
    create_cost as create_cost_svc,
)
from app.services.cost_service import (
    delete_cost as delete_cost_svc,
)
from app.services.cost_service import (
    get_cost as get_cost_svc,
)

router = APIRouter()


@router.post("/costs", response_model=CostOfLiving)
async def create_cost(
    cost: CostOfLivingCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return create_cost_svc(db=db, payload=cost)


@router.get("/{cost_id}", response_model=CostOfLiving)
async def read_cost(
    cost_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    db_cost = get_cost_svc(db, cost_id=cost_id)
    if db_cost is None:
        raise HTTPException(status_code=404, detail="Cost not found")
    return db_cost


@router.delete("/{cost_id}")
async def delete_cost(
    cost_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(AdminOnly),
):
    success = delete_cost_svc(db, cost_id=cost_id)
    if not success:
        raise HTTPException(status_code=404, detail="Cost not found")
    return {"detail": "Cost deleted"}
