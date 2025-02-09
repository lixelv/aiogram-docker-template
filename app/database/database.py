from .context import PostgresConnectionWithContext
from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel
from core.decorators import async_logfire_class_decorator


class User(BaseModel):
    id: int
    username: str
    full_name: str
    timestamp: datetime


@async_logfire_class_decorator
class PostgresDB(PostgresConnectionWithContext):
    async def create_user(self) -> None:
        query = "INSERT INTO users (id, username, full_name) VALUES ($1, $2, $3)"
        await self.execute(
            query,
            (
                self.context.user.id,
                self.context.user.username,
                self.context.user.full_name,
            ),
        )

    async def get_user(self) -> Optional[User]:
        query = "SELECT * FROM users WHERE id=$1"
        result = await self.fetch_one(query, (self.context.user.id,), User)

        return result

    async def get_all_users(self) -> Optional[List[User]]:
        query = "SELECT * FROM users"
        result = await self.fetch_all(query, (), User)

        return result
