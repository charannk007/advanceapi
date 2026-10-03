from fastapi import APIRouter, HTTPException 

from app.schemas.product import ProductCreate , ProductResponse
from app.services.product_service import create_product , get_products , get_product , update_product,delete_product

router = APIRouter(
    prefix="/products",
    tags=["products"],
)

@router.post("/", response_model=ProductResponse)
async def create_product_endpoint(product: ProductCreate):
    return await create_product(product)

@router.get("/", response_model=list[ProductResponse])
async def get_products_endpoint():
    return await get_products()


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product_endpoint(product_id: int):
    product = await get_product(product_id)
    if product is None:
        return {"error": "Product not found"}
    return product

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product_endpoint(product_id: int, product: ProductCreate):
    updated_product = await update_product(product_id, product)
    if updated_product is None:
        return {"error": "Product not found"}
    return updated_product

@router.delete("/{product_id}")
async def delete_product_endpoint(product_id: int):
    deleted = await delete_product(product_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return {
        "message": "Product deleted successfully",
        "product_id": product_id,
    }