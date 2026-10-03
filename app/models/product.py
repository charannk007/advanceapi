from app.database.connection import get_db_connection


async def create_products_table():
    connection = await get_db_connection()

    await connection.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            price FLOAT NOT NULL
        )
    """)

    await connection.close()


import asyncio

asyncio.run(create_products_table())