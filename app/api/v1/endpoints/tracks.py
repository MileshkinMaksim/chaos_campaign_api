from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.models.force import ForceModel
from app.dependencies.campaign import verify_force_ownership
from app.schemas.track import TrackCompletionRequest, TrackCompletionResponse
from app.services.track_service import TrackService

router = APIRouter()


@router.post("/{track_id}/start", summary="Старт миссии/трека")
async def start_track(
    track_id: str,
    entry_cost_wp: int = Query(100, ge=0, description="Стоимость входа в WP"),
    force_id: str = Query(...),
    force: ForceModel = Depends(verify_force_ownership),
    db: AsyncSession = Depends(get_db)
):
    """
    Списывает оговоренные Warchest Points за участие в треке.
    
    * **400 Bad Request**: Недостаточно WP (`InsufficientWarchestPointsError`).
    """
    updated_force = await TrackService.start_track(db=db, force=force, entry_cost_wp=entry_cost_wp)
    return {"status": "track_started", "track_id": track_id, "remaining_wp": updated_force.warchest_points}


@router.post("/{track_id}/complete", response_model=TrackCompletionResponse, summary="Подведение итогов миссии")
async def complete_track(
    track_id: str,
    request: TrackCompletionRequest,
    earned_wp: int = Query(300, ge=0),
    earned_sp: int = Query(150, ge=0),
    force_id: str = Query(...),
    force: ForceModel = Depends(verify_force_ownership),
    db: AsyncSession = Depends(get_db)
):
    """
    Транзакционное подведение итогов трека:
    1. Перевод SP в XP пилотов (до 200 SP на группу).
    2. Бонус +50 XP для MVP.
    3. Выплата наград в WP/SP.
    4. Изменение статусов повреждений техники.
    """
    return await TrackService.complete_track(
        db=db,
        force=force,
        track_id=track_id,
        earned_wp=earned_wp,
        earned_sp=earned_sp,
        request=request
    )