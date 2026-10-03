import asyncpg

from app.core.config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
)


pool: asyncpg.Pool | None = None


async def create_db_pool():
    global pool

    pool = await asyncpg.create_pool(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


async def close_db_pool():
    global pool

    if pool:
        await pool.close()
        pool = None


async def get_db_connection():
    if pool is None:
        raise RuntimeError("Database pool is not initialized")

    return await pool.acquire()