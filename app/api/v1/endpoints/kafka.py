from fastapi import APIRouter, Depends

from app.core.dependencies import get_current_active_user
from app.models.user import User
from app.schemas.kafka import KafkaMessage, KafkaPublishResponse
from app.services.consumer_service import KafkaService

router = APIRouter(
    prefix="/kafka",
    tags=["kafka"],
)


@router.post("/publish", response_model=KafkaPublishResponse)
async def publish_kafka_message(
    data: KafkaMessage,
    current_user: User = Depends(get_current_active_user),
) -> KafkaPublishResponse:
    return await KafkaService.publish_message(
        data=data,
        current_user=current_user,
    )
