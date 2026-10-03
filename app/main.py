from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database.connection import create_db_pool, close_db_pool
from app.routers.products import router as product_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_pool()

    yield

    await close_db_pool()


app = FastAPI(
    title="Learning FastAPI",
    description="Modular FastAPI Learning Project",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(product_router)


@app.get("/")
async def home():
    return {"message": "Welcome to Modular FastAPI"}