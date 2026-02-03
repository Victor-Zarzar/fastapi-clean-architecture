from sqlalchemy.orm import Session

from app.models.costs import Cost
from app.schemas.costs import CostOfLivingCreate


def create_cost(db: Session, payload: CostOfLivingCreate) -> Cost:
    obj = Cost(
        title=payload.title,
        category=payload.category,
        amount=payload.amount,
        currency=payload.currency,
        city=payload.city,
        country=payload.country,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_cost(db: Session, cost_id: int) -> Cost | None:
    return db.get(Cost, cost_id)


def delete_cost(db: Session, cost_id: int) -> bool:
    obj = db.get(Cost, cost_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
