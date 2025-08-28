import redis # type: ignore
from app.config.env import ENV

redis_client = redis.Redis(
    host=ENV.redis_host,
    port=ENV.redis_port,
    db=ENV.redis_db,
    decode_responses=True
)