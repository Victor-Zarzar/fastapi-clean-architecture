import asyncio
import json

from aiokafka import AIOKafkaConsumer

from app.core.config import settings


class KafkaConsumer:
    def __init__(self):
        self._consumer = None
        self._consumer_task = None
        self._is_running = False

    async def start(self):
        self._consumer = AIOKafkaConsumer(
            settings.KAFKA_TOPIC,
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            group_id=settings.KAFKA_CONSUMER_GROUP,
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
            auto_offset_reset="latest",
        )
        await self._consumer.start()
        self._is_running = True
        self._consumer_task = asyncio.create_task(self._consume())

    async def _consume(self):
        try:
            async for msg in self._consumer:
                print(f"[→] {msg.topic} | offset: {msg.offset} | value: {msg.value}")
                if not self._is_running:
                    break
        except Exception as error:
            print(f"Kafka consumption error: {error}")

    async def stop(self):
        self._is_running = False
        if self._consumer:
            await self._consumer.stop()
        if self._consumer_task:
            self._consumer_task.cancel()


consumer = KafkaConsumer()
