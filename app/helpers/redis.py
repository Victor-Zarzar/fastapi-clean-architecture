from datetime import UTC, datetime

import redis.asyncio as redis
from redis import Redis as redis1
from rq import Queue

from app.core.config import settings


class RedisManager:
    def __init__(self) -> None:
        self.pool = redis.ConnectionPool(
            host=settings.REDIS_LOCATION,
            port=settings.REDIS_PORT,
            decode_responses=True,
        )

    def get_client(self) -> redis.Redis:
        return redis.Redis(connection_pool=self.pool)

    async def check_if_jwt_exists(self, token: str) -> bool:
        conn = self.get_client()
        result = await conn.exists(token)
        return bool(result)

    async def put_jwt_redis(self, token: str, exp: int):

        conn = self.get_client()
        now = int(datetime.now(UTC).timestamp())
        ttl = exp - now
        if ttl > 0:
            await conn.set(token, 1, ex=ttl)

    async def blacklist_token(self, token: str, exp: int):

        conn = self.get_client()

        now = int(datetime.now(UTC).timestamp())
        ttl = exp - now

        if ttl > 0:
            await conn.set(f"blacklist:{token}", "1", ex=ttl)

    async def is_token_blacklisted(self, token: str) -> bool:
        conn = self.get_client()
        result = await conn.exists(f"blacklist:{token}")
        return bool(result)

    async def init_rq_queue(self):
        try:
            queue = Queue(
                connection=redis1(
                    host=settings.REDIS_LOCATION,
                    port=settings.REDIS_PORT,
                )
            )
            return queue
        except Exception as e:
            raise e

    async def store_validation_token(
        self, email: str, name: str, token: str, expire: int = 86400
    ):
        try:
            conn = redis.Redis(connection_pool=self.pool)
            await conn.set(token, f"{name}:{email}", ex=expire)
        except redis.ConnectionError as err:
            raise err

    async def store_changepass_token(self, email: str, token: str, expire: int = 180):
        hashed_token = str(hash((email, token)))
        try:
            conn = redis.Redis(connection_pool=self.pool)
            await conn.set(hashed_token, f"{token}:{email}", ex=expire)
        except redis.ConnectionError as err:
            raise err

    async def get_token(self, token):
        try:
            conn = redis.Redis(connection_pool=self.pool)
            value = await conn.get(token)
            return value
        except redis.ConnectionError as err:
            raise err
