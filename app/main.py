import time
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from app.config import settings
from app.core.exceptions import (
    InsufficientXPError,
    InsufficientSupportPointsError,
    ReputationRequirementNotMetError,
    InvalidStartingForceConfigError,
)
from app.api.v1.api import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.exception_handler(InsufficientXPError)
async def insufficient_xp_handler(request: Request, exc: InsufficientXPError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.message, "error_code": "INSUFFICIENT_XP"}
    )


@app.exception_handler(InsufficientSupportPointsError)
async def insufficient_sp_handler(request: Request, exc: InsufficientSupportPointsError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.message, "error_code": "INSUFFICIENT_SUPPORT_POINTS"}
    )


@app.exception_handler(ReputationRequirementNotMetError)
async def reputation_handler(request: Request, exc: ReputationRequirementNotMetError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.message, "error_code": "REPUTATION_REQUIREMENT_NOT_MET"}
    )


@app.exception_handler(InvalidStartingForceConfigError)
async def invalid_force_handler(request: Request, exc: InvalidStartingForceConfigError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.message, "error_code": "INVALID_STARTING_FORCE_CONFIG"}
    )


app.include_router(api_router, prefix=settings.API_V1_STR)