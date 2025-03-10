from typing import Optional

from .context import PostgresConnectionWithContext
from .models import User
from core import async_logfire_class_decorator


@async_logfire_class_decorator
class UserMethods(PostgresConnectionWithContext):
    async def create_user(self) -> None:
        query = "INSERT INTO users (id, username, full_name, language_code) VALUES ($1, $2, $3, $4)"
        await self.execute(
            query,
            (
                self.context.user.id,
                self.context.user.username,
                self.context.user.full_name,
                self.context.user.language_code,
            ),
        )

    async def get_user(self) -> Optional[User]:
        query = "SELECT * FROM users WHERE id=$1"
        return await self.fetch_one(query, (self.context.user.id,), User)


class PostgresDB(UserMethods):
    pass
