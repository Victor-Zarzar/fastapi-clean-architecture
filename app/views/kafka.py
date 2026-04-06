from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.dependencies import get_current_active_user
from app.db.database import get_db
from app.helpers.producer import producer
from app.models.user import User
from app.schemas.kafka import KafkaMessage

router = APIRouter()


@router.post("/publish")
async def publish_kafka_message(
    data: KafkaMessage,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    message = {"key": data.key, "value": data.value}

    await producer.send(settings.KAFKA_TOPIC, message)

    return {
        "sent": True,
        "payload": message,
        "user": current_user.username,
    }
