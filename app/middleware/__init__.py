from aiogram import Dispatcher

from .database import DatabaseMiddleware
from .logging import LoggingMiddleware


def setup_middleware(dp: Dispatcher) -> None:
    dp.message.middleware(DatabaseMiddleware())
    dp.message.middleware(LoggingMiddleware())


__all__ = ["setup_middleware", "DatabaseMiddleware", "LoggingMiddleware"]
