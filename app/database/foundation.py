import asyncpg

from pydantic import BaseModel
from typing import Optional, List, TypeVar, Type

T = TypeVar("T", bound=BaseModel)


class PostgresPool:
    def __init__(self, config: dict):
        self.config = config
        self.pool: Optional[asyncpg.Pool] = None

    def __str__(self):
        return f"PostgresPool({self.config['database']})"

    async def __aenter__(self):
        self.pool = await asyncpg.create_pool(**self.config)
        await self.create_tables()

        return self

    async def __aexit__(self, *exc):
        await self.pool.close()

    async def create_tables(self) -> None:
        with open("app/database/schema.sql", "r") as f:
            query = f.read()

        async with self.pool.acquire() as connection:
            await self.execute(connection, query, transaction=True)

    async def execute(
        self, connection, query: str, values=(), transaction=False
    ) -> None:
        if transaction:
            async with connection.transaction():
                await connection.execute(query, *values)
        else:
            await connection.execute(query, *values)

    async def fetch_one(
        self,
        connection,
        query: str,
        values=(),
        pydantic_model: Optional[Type[T]] = None,
    ) -> Optional[T]:
        result = await self.fetch_all(connection, query, values, pydantic_model)
        return result[0] if result else None

    async def fetch_all(
        self,
        connection,
        query: str,
        values=(),
        pydantic_model: Optional[Type[T]] = None,
    ) -> Optional[List[T]]:
        rows = await connection.fetch(query, *values)

        using_model = pydantic_model or dict
        return [using_model(**r) for r in rows] if rows else None
