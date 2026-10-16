import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request

from app.api.v1.api import api_router
from app.config import settings
from app.core.exceptions import ChaosCampaignException, chaos_campaign_exception_handler
from app.db.database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление подключением к СУБД."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="REST API менеджер кампании BattleTech Classic (Hot Spots: Draconis Reach)",
    lifespan=lifespan,
)

app.add_exception_handler(ChaosCampaignException, chaos_campaign_exception_handler)

# Подключение роутера API V1
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.4f}s"
    return response


@app.get("/health", tags=["Health Check"])
async def health_check():
    return {"status": "ok", "project": settings.PROJECT_NAME, "version": settings.VERSION}