import logfire

from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Any, Dict, Callable, Awaitable


class UserExistenceCheckMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        db = data["db"]

        if not await db.user_exists(event.from_user.id):
            logfire.info(
                "New user: {username}",
                user_id=event.from_user.id,  # добавьте полезные данные
                user_full_name=event.from_user.full_name,
                username=event.from_user.username,
            )
            await db.create_user(
                event.from_user.id,
                event.from_user.username,
                event.from_user.full_name,
            )

        return await handler(event, data)
