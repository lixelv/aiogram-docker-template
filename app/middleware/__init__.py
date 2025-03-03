from aiogram import Dispatcher

from .context import ContextMiddleware
from .postgres import DatabaseMiddleware
from .logging import LoggingMiddleware


def setup_middleware(dp: Dispatcher) -> None:
    for middleware in (dp.message, dp.callback_query):
        middleware.outer_middleware(ContextMiddleware())
        middleware.outer_middleware(LoggingMiddleware())
        middleware.outer_middleware(DatabaseMiddleware())


__all__ = [
    "setup_middleware",
    "ContextMiddleware",
    "LoggingMiddleware",
    "DatabaseMiddleware",
]
