from time import perf_counter

from sqlalchemy.orm import Session

from app.models.user import User
from app.repository.health import HealthRepository
from app.schemas.health import HealthCheckOut


class HealthService:
    @staticmethod
    def execute(db: Session, current_user: User) -> HealthCheckOut:
        start = perf_counter()
        db_ok = HealthRepository.check_database(db)
        elapsed = perf_counter() - start
        status = "ok" if db_ok else "error"
        message = "service healthy" if db_ok else "database unavailable"
        return HealthCheckOut(
            status=status,
            message=message,
            details=f"user={current_user.username}, role={current_user.role}",
            response_time=elapsed,
        )
