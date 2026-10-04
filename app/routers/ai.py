from fastapi import APIRouter

from app.services.ai_service import ask_ai
from app.services.product_service import get_product_by_name

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


@router.post("/chat")
async def chat(message: str):
    product_name = await ask_ai(message)

    product = await get_product_by_name(product_name)

    if product is None:
        return {
            "message": f"Product '{product_name}' not found"
        }

    return {
        "product": product
    }