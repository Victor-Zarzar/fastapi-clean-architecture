from app.helpers.redis import RedisManager

redis = RedisManager()


def get_redis() -> RedisManager:
    return redis
