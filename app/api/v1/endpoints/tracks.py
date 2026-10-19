from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.db.models.force import ForceModel
from app.dependencies.campaign import verify_force_ownership
from app.schemas.track import TrackCompletionRequest, TrackCompletionResponse
from app.services.track_service import TrackService

router = APIRouter()


@router.post("/{track_id}/start", summary="Старт трека миссии")
async def start_track(
    track_id: str,
    entry_cost_sp: int = Query(100, ge=0),
    force: ForceModel = Depends(verify_force_ownership),
    db: AsyncSession = Depends(get_db)
):
    return await TrackService.start_track(db=db, force=force, entry_cost_sp=entry_cost_sp)


@router.post("/{track_id}/complete", response_model=TrackCompletionResponse, summary="Подведение итогов миссии")
async def complete_track(
    track_id: str,
    request: TrackCompletionRequest,
    earned_sp: int = Query(150, ge=0),
    force: ForceModel = Depends(verify_force_ownership),
    db: AsyncSession = Depends(get_db)
):
    return await TrackService.complete_track(
        db=db,
        force=force,
        track_id=track_id,
        earned_sp=earned_sp,
        request=request
    )