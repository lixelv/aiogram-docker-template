import logfire

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Any, Dict, Callable, Awaitable

from database import PostgresDB


class IsBannedMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        db: PostgresDB = data["db"]
        user = await db.get_user()

        if not user.is_banned:
            logfire.info("User is not banned!")
            return await handler(event, data)

        logfire.info("User is banned!")
        return await event.reply("You are banned!")
