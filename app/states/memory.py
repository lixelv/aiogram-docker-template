from aiogram.fsm.storage.redis import RedisStorage
from redis.client import Redis

from core import REDIS_CONFIG

redis = Redis(**REDIS_CONFIG)
storage = RedisStorage(redis)
