from aiogram.types import Message
from typing import Any, Dict, Callable, Awaitable
from database import PostgresDB
from aiogram import BaseMiddleware
from abc import abstractmethod


class DatabaseRelatedMiddleware(BaseMiddleware):
    def __init__(self, db: PostgresDB):
        super().__init__()
        self.db = db

    @abstractmethod
    async def __call__(self, handler, event, data):
        pass


class UserCheckMiddleware(DatabaseRelatedMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if not await self.db.user_exists(event.from_user.id):
            await self.db.create_user(
                event.from_user.id,
                event.from_user.username,
                event.from_user.full_name,
            )

        return await handler(event, data)
