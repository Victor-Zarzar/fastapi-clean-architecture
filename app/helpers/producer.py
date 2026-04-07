import json

from aiokafka import AIOKafkaProducer

from app.core.config import settings


class KafkaProducer:
    def __init__(self):
        self._producer = None

    async def start(self):
        self._producer = AIOKafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
        await self._producer.start()

    async def stop(self):
        if self._producer:
            await self._producer.stop()

    async def send(self, topic: str, message: dict):
        if self._producer:
            await self._producer.send_and_wait(topic, message)


producer = KafkaProducer()
