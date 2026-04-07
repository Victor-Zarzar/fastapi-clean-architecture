from fastapi import APIRouter

from app.api.v1.endpoints.admin import router as admin_router
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.costs import router as costs_router
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.kafka import router as kafka_router
from app.api.v1.endpoints.user import router as user_router

routers = APIRouter()

router_list = [
    auth_router,
    user_router,
    admin_router,
    costs_router,
    kafka_router,
    health_router,
]

for router in router_list:
    routers.include_router(router)
