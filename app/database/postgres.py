from typing import Optional, List

from .context import PostgresConnectionWithContext
from .models import User
from core import async_logfire_class_decorator


@async_logfire_class_decorator
class UserMethods(PostgresConnectionWithContext):
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
        return await self.fetch_one(query, (self.context.user.id,), User)

    async def get_user_by_id(self, user_id) -> Optional[User]:
        query = "SELECT * FROM users WHERE id=$1"
        return await self.fetch_one(query, (user_id,), User)

    async def get_user_by_username(self, username) -> Optional[User]:
        query = "SELECT * FROM users WHERE username=$1"
        return await self.fetch_one(query, (username,), User)

    # Using index system (0 is the first element)
    async def get_all_users(self, limit, offset) -> Optional[List[User]]:
        offset = offset * limit
        query = "SELECT * FROM users LIMIT $1 OFFSET $2"
        return await self.fetch_all(query, (limit, offset), User)

    async def update_user_is_admin(self, user_id, is_admin: bool) -> None:
        query = "UPDATE users SET is_admin=$1 WHERE id=$2"
        await self.execute(query, (is_admin, user_id))


class PostgresDB(UserMethods):
    pass
