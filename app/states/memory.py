from aiogram.fsm.storage.redis import RedisStorage
<<<<<<< HEAD
from redis.asyncio.client import Redis
=======
from redis.client import Redis
>>>>>>> 61d6c2f (Added redis, not tested yet)

from core import REDIS_CONFIG

redis = Redis(**REDIS_CONFIG)
storage = RedisStorage(redis)
