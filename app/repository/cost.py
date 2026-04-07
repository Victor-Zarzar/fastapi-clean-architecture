from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models.costs import Cost


class CostRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, payload: dict) -> Cost:
        cost = Cost(**payload)
        self.db.add(cost)
        self.db.commit()
        self.db.refresh(cost)
        return cost

    def get_all(self) -> list[Cost]:
        result = self.db.execute(select(Cost))
        return result.scalars().all()

    def get_by_id(self, cost_id: int) -> Cost | None:
        result = self.db.execute(select(Cost).where(Cost.id == cost_id))
        return result.scalar_one_or_none()

    def delete(self, cost_id: int) -> bool:
        result = self.db.execute(delete(Cost).where(Cost.id == cost_id))
        self.db.commit()
        return result.rowcount > 0
