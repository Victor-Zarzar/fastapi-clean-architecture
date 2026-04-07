from fastapi import APIRouter, Depends

from app.core.dependencies import AdminOnly, get_cost_service, get_current_active_user
from app.models.user import User
from app.schemas.costs import CostOfLiving, CostOfLivingCreate
from app.services.cost_service import CostService

router = APIRouter(
    prefix="/costs",
    tags=["costs"],
)


@router.post("", response_model=CostOfLiving)
def create_cost(
    cost: CostOfLivingCreate,
    service: CostService = Depends(get_cost_service),
    current_user: User = Depends(get_current_active_user),
):
    return service.create(cost)


@router.get("", response_model=list[CostOfLiving])
def read_costs(
    service: CostService = Depends(get_cost_service),
    current_user: User = Depends(get_current_active_user),
):
    return service.get_all()


@router.get("/{cost_id}", response_model=CostOfLiving)
def read_cost(
    cost_id: int,
    service: CostService = Depends(get_cost_service),
    current_user: User = Depends(get_current_active_user),
):
    return service.get_by_id(cost_id)


@router.delete("/{cost_id}")
def delete_cost(
    cost_id: int,
    service: CostService = Depends(get_cost_service),
    current_user: User = Depends(AdminOnly),
):
    service.delete(cost_id)
    return {"detail": "Cost deleted"}
