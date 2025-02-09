from aiogram import Dispatcher

from .context import ContextMiddleware
from .database import DatabaseMiddleware
from .logging import LoggingMiddleware


def setup_middleware(dp: Dispatcher) -> None:
    dp.message.outer_middleware(ContextMiddleware())
    dp.message.outer_middleware(LoggingMiddleware())
    dp.message.outer_middleware(DatabaseMiddleware())


__all__ = [
    "setup_middleware",
    "ContextMiddleware",
    "LoggingMiddleware",
    "DatabaseMiddleware",
]
