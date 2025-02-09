import asyncpg

from typing import Optional


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
            await self.do(connection, query, transaction=True)

    async def do(self, connection, query: str, values=None, transaction=False) -> None:
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

    async def read(
        self, connection, query: str, values=None, one=False
    ) -> Optional[dict]:
        rows = (
            await connection.fetch(query, *values)
            if values
            else await connection.fetch(query)
        )
        if one:
            result = dict(rows[0]) if rows else None
        else:
            result = [dict(r) for r in rows]

        return result
