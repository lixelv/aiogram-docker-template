from aiogram import Dispatcher

from .user_exists import UserExistenceCheckMiddleware


def setup_middleware(dp: Dispatcher) -> None:
    dp.message.middleware(UserExistenceCheckMiddleware())


__all__ = ["setup_middleware", "UserExistenceCheckMiddleware"]
