import time
import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers.ai import router as ai_router
from app.core.security import security
from app.database.connection import create_db_pool, close_db_pool
from app.routers.products import router as product_router
from app.core.exception import ProductNotFoundException
from app.core.exception_handlers import product_not_found_handler


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

app.add_exception_handler(
    ProductNotFoundException,
    product_not_found_handler,
)


@app.middleware("http")
async def timing_middleware(request, call_next):
    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time

    print(
        f"{request.method} {request.url.path} "
        f"completed in {duration:.4f} seconds"
    )

    return response


@app.middleware("http")
async def request_id_middleware(request, call_next):
    request_id = str(uuid.uuid4())

    response = await call_next(request)

    response.headers["X-Request-ID"] = request_id

    print(f"Request ID: {request_id}")

    return response

app.include_router(product_router)
app.include_router(ai_router)

@app.get("/")
async def home():
    return {"message": "Welcome to Modular FastAPI"}


