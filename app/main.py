from fastapi import FastAPI

from app.routers.products import router as products_router

app = FastAPI(
    title="Products API",
    description="API for managing products",
    version="1.0.0",
)

app.include_router(products_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Products API!"}

