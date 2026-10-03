from app.database.connection import get_db_connection, pool
from app.schemas.product import ProductCreate


async def create_product(product: ProductCreate):
    connection = await get_db_connection()

    try:
        row = await connection.fetchrow(
            """
            INSERT INTO products (name, price)
            VALUES ($1, $2)
            RETURNING id, name, price
            """,
            product.name,
            product.price,
        )

        return dict(row)

    finally:
        await pool.release(connection)

async def get_products():
    connection = await get_db_connection()

    try:
        rows = await connection.fetch(
            """
            SELECT id, name, price
            FROM products
            ORDER BY id
            """
        )

        return [dict(row) for row in rows]

    finally:
        await pool.release(connection)


async def get_product(product_id: int):
    connection = await get_db_connection()

    try:
        row = await connection.fetchrow(
            """
            SELECT id, name, price
            FROM products
            WHERE id = $1
            """,
            product_id,
        )

        if row is None:
            return None

        return dict(row)

    finally:
        await pool.release(connection)


async def update_product(product_id: int, product: ProductCreate):
    connection = await get_db_connection()

    try:
        row = await connection.fetchrow(
            """
            UPDATE products
            SET name = $1, price = $2
            WHERE id = $3
            RETURNING id, name, price
            """,
            product.name,
            product.price,
            product_id,
        )

        if row is None:
            return None

        return dict(row)

    finally:
        await pool.release(connection)


async def delete_product(product_id: int):
    connection = await get_db_connection()

    try:
        row = await connection.fetchrow(
            """
            DELETE FROM products
            WHERE id = $1
            RETURNING id
            """,
            product_id,
        )

        if row is None:
            return False

        return True

    finally:
        await pool.release(connection)