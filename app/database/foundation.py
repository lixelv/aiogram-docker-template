import asyncpg

from typing import Optional, List


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
        self, connection, query: str, values=None, transaction=False
    ) -> None:
        if transaction:
            async with connection.transaction():
                if values:
                    await connection.execute(query, *values)
                else:
                    await connection.execute(query)
        else:
            if values:
                await connection.execute(query, *values)
            else:
                await connection.execute(query)

    async def fetch_one(
        self, connection, query: str, values=None, pydantic_model=None
    ) -> Optional[dict]:
        return await self._fetch(
            connection, query, values, one=True, pydantic_model=pydantic_model
        )

    async def fetch_all(
        self, connection, query: str, values=None, pydantic_model=None
    ) -> Optional[List[dict]]:
        return await self._fetch(
            connection, query, values, one=False, pydantic_model=pydantic_model
        )

    async def _fetch(
        self, connection, query: str, values=None, one=False, pydantic_model=None
    ) -> Optional[dict] | Optional[List[dict]]:
        rows = (
            await connection.fetch(query, *values)
            if values
            else await connection.fetch(query)
        )
        if one:
            result = dict(rows[0]) if rows else None

            if pydantic_model is not None and result is not None:
                result = pydantic_model(**result)
        else:
            result = [dict(r) for r in rows]

            if pydantic_model is not None:
                result = [pydantic_model(**r) for r in result]

            if not result:
                result = None

        return result
