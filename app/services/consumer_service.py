from app.core.config import settings
from app.models.user import User
from app.repository.kafka import KafkaRepository
from app.schemas.kafka import KafkaMessage, KafkaPublishResponse


class KafkaService:
    @staticmethod
    async def publish_message(
        data: KafkaMessage,
        current_user: User,
    ) -> KafkaPublishResponse:
        message = {
            "key": data.key,
            "value": data.value,
        }

        await KafkaRepository.publish(
            topic=settings.KAFKA_TOPIC,
            message=message,
        )

        return KafkaPublishResponse(
            sent=True,
            payload=KafkaMessage(**message),
            user=current_user.username,
        )


consumer = KafkaService()
