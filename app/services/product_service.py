from app.database import connection
from app.schemas.product import ProductCreate
from app.core.exception import ProductNotFoundException


async def create_product(product: ProductCreate):
    db_connection = await connection.get_db_connection()

    try:
        row = await db_connection.fetchrow(
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
        await connection.pool.release(db_connection)


async def create_products(products: list[ProductCreate]):
    db_connection = await connection.get_db_connection()

    try:
        rows = await db_connection.fetch(
            """
            INSERT INTO products (name, price)
            SELECT name, price
            FROM UNNEST($1::text[], $2::float8[])
            AS data(name, price)
            RETURNING id, name, price
            """,
            [product.name for product in products],
            [product.price for product in products],
        )

        return [dict(row) for row in rows]

    finally:
        await connection.pool.release(db_connection)


async def get_products():
    db_connection = await connection.get_db_connection()

    try:
        rows = await db_connection.fetch(
            """
            SELECT id, name, price
            FROM products
            ORDER BY id
            """
        )

        return [dict(row) for row in rows]

    finally:
        await connection.pool.release(db_connection)


async def get_product(product_id: int):
    db_connection = await connection.get_db_connection()

    try:
        row = await db_connection.fetchrow(
            """
            SELECT id, name, price
            FROM products
            WHERE id = $1
            """,
            product_id,
        )

        if row is None:
            raise ProductNotFoundException(product_id=product_id)

        return dict(row)

    finally:
        await connection.pool.release(db_connection)


async def update_product(product_id: int, product: ProductCreate):
    db_connection = await connection.get_db_connection()

    try:
        row = await db_connection.fetchrow(
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
            raise ProductNotFoundException(product_id=product_id)

        return dict(row)

    finally:
        await connection.pool.release(db_connection)


async def delete_product(product_id: int):
    db_connection = await connection.get_db_connection()

    try:
        row = await db_connection.fetchrow(
            """
            DELETE FROM products
            WHERE id = $1
            RETURNING id
            """,
            product_id,
        )

        if row is None:
            raise ProductNotFoundException(product_id=product_id)

        return True

    finally:
        await connection.pool.release(db_connection)

async def get_product_by_name(name: str):
    db_connection = await connection.get_db_connection()

    try:
        row = await db_connection.fetchrow(
            """
            SELECT id, name, price
            FROM products
            WHERE LOWER(name) = LOWER($1)
            """,
            name,
        )

        if row is None:
            return None

        return dict(row)

    finally:
        await connection.pool.release(db_connection)