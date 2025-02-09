from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update
from typing import Any, Dict, Callable, Awaitable

from database import Context


class ContextMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        update: Update = data["event_update"]

        data["context"] = Context(
            user=event.from_user,
            update_id=update.update_id,
            event_type=event.__class__.__name__.lower(),
        )

        return await handler(event, data)
