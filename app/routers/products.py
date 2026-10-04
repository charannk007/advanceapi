from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials

from app.core.security import security, verify_token
from app.schemas.product import ProductCreate, ProductResponse
from app.services.product_service import (
    create_product,
    create_products,
    get_products,
    get_product,
    update_product,
    delete_product,
)


router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.post("/", response_model=ProductResponse)
async def create_product_endpoint(
    product: ProductCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    verify_token(credentials)

    return await create_product(product)

@router.post("/bulk")
async def create_products_endpoint(
    products: list[ProductCreate],
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    verify_token(credentials)

    return await create_products(products)


@router.get("/", response_model=list[ProductResponse])
async def get_products_endpoint(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    verify_token(credentials)

    return await get_products()


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product_endpoint(
    product_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    verify_token(credentials)

    return await get_product(product_id)


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product_endpoint(
    product_id: int,
    product: ProductCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    verify_token(credentials)

    return await update_product(product_id, product)


@router.delete("/{product_id}")
async def delete_product_endpoint(
    product_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    verify_token(credentials)
    await delete_product(product_id)
    return {
        "message": "Product deleted successfully",
        "product_id": product_id,
    }