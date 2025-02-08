from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Any, Dict, Callable, Awaitable

from database import PostgresDB


class DatabaseMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        db: PostgresDB = data["db"]
        db.add_context("user_id", event.from_user.id)

        if not await db.user_exists():
            await db.create_user(
                event.from_user.username,
                event.from_user.full_name,
            )

        result = await handler(event, data)
        db.clear_context()
        return result
