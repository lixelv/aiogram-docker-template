from aiogram import Dispatcher

from .context import ContextMiddleware
from .postgres import DatabaseMiddleware
from .logging import LoggingMiddleware
from .lexicon import LexiconMiddleware


def setup_middlewares(dp: Dispatcher) -> None:
    for middleware in (dp.message, dp.callback_query):
        middleware.outer_middleware(ContextMiddleware())
        middleware.outer_middleware(LoggingMiddleware())
        middleware.outer_middleware(DatabaseMiddleware())
        middleware.outer_middleware(LexiconMiddleware())


__all__ = [
    "setup_middlewares",
    "ContextMiddleware",
    "LoggingMiddleware",
    "DatabaseMiddleware",
    "LexiconMiddleware",
]
