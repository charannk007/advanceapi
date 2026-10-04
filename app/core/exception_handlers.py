from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exception import ProductNotFoundException


async def product_not_found_handler(
    request: Request,
    exc: ProductNotFoundException,
):
    return JSONResponse(
        status_code=404,
        content={
            "detail": str(exc),
            "product_id": exc.product_id,
        },
    )