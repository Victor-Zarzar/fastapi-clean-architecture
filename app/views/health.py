from time import perf_counter

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import AdminOnly, get_db
from app.models.user import User
from app.schemas.health import HealthCheckOut

router = APIRouter()


@router.get("/health", response_model=HealthCheckOut)
async def health_check(
    current_user: User = Depends(AdminOnly),
    db: AsyncSession = Depends(get_db),
):
    start = perf_counter()

    db.execute("SELECT 1")

    elapsed = perf_counter() - start

    # You don't need to record in the database for a health check.
    # If you want to log each check, uncomment the block below.
    # rec = HealthCheckORM(
    #     status="ok",
    #     message="service healthy",
    #     details=f"user={current_user.username}, role={current_user.role}",
    #     response_time=elapsed,
    # )
    # db.add(rec)
    # db.commit()
    # db.refresh(rec)
    # return rec

    return HealthCheckOut(
        status="ok",
        message="service healthy",
        details=f"user={current_user.username}, role={current_user.role}",
        response_time=elapsed,
    )
