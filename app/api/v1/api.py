from fastapi import APIRouter
from app.api.v1.endpoints import auth, contracts, forces, generator, logistics, pilots, tracks

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(forces.router, prefix="/forces", tags=["Forces"])
api_router.include_router(pilots.router, prefix="/pilots", tags=["Pilots"])
api_router.include_router(contracts.router, prefix="/contracts", tags=["Contracts"])
api_router.include_router(tracks.router, prefix="/tracks", tags=["Tracks"])
api_router.include_router(logistics.router, prefix="/logistics", tags=["Logistics"])
api_router.include_router(generator.router, prefix="/generator", tags=["Generator"])