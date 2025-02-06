import asyncpg
import logfire

from typing import Optional


class PostgresFoundation:
    def __init__(self, config: dict):
        self.config = config
        self.pool: Optional[asyncpg.Pool] = None

    async def __aenter__(self):
        self.pool = await asyncpg.create_pool(**self.config)
        await self.create_tables()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.pool.close()

    async def create_tables(self) -> None:
        with open("app/database/schema.sql", "r") as f:
            sql = f.read()

        await self.do(sql, transaction=True)

    async def do(self, sql: str, values=None, transaction=False, log=True) -> None:
        async with self.pool.acquire() as conn:
            if log:
                if values:
                    logfire.info("Executing:\n" + sql, args=values)
                else:
                    logfire.info("Executing:\n" + sql)

            if transaction:
                async with conn.transaction():
                    if values:
                        await conn.execute(sql, *values)
                    else:
                        await conn.execute(sql)
            else:
                if values:
                    await conn.execute(sql, *values)
                else:
                    await conn.execute(sql)

            if log:
                logfire.info("Executed successfully!")

    async def read(self, sql: str, values=None, one=False, log=True) -> Optional[dict]:
        if log:
            if values:
                logfire.info("Fetching:\n" + sql, args=values)
            else:
                logfire.info("Fetching:\n" + sql)

        async with self.pool.acquire() as conn:
            rows = await conn.fetch(sql, *values) if values else await conn.fetch(sql)
            if one:
                result = dict(rows[0]) if rows else None
            result = [dict(r) for r in rows]

        if log:
            logfire.info("Fetched data successfully!", data=result)

        return result
