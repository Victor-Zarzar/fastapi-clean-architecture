from app.core.execeptions import NotFoundError
from app.repository.cost import CostRepository
from app.schemas.costs import CostOfLivingCreate


class CostService:
    def __init__(self, repository: CostRepository):
        self.repository = repository

    def create(self, payload: CostOfLivingCreate):
        return self.repository.create(payload.model_dump())

    def get_all(self):
        return self.repository.get_all()

    def get_by_id(self, cost_id: int):
        cost = self.repository.get_by_id(cost_id)
        if not cost:
            raise NotFoundError("Cost not found")
        return cost

    def delete(self, cost_id: int):
        success = self.repository.delete(cost_id)
        if not success:
            raise NotFoundError("Cost not found")
