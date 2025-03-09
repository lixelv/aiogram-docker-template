# from aiogram.fsm.storage.base import BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage


# TODO must be implemented, now it is just a placeholder
class RedisStorage(MemoryStorage):
    pass


storage = RedisStorage()
