from sqlalchemy import text
from sqlalchemy.orm import Session


class HealthRepository:
    @staticmethod
    def check_database(db: Session) -> bool:
        result = db.execute(text("SELECT 1"))
        value = result.scalar_one_or_none()
        return value == 1
