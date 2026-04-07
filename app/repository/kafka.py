from app.helpers.producer import producer


class KafkaRepository:
    @staticmethod
    async def publish(topic: str, message: dict) -> None:
        await producer.send(topic, message)
