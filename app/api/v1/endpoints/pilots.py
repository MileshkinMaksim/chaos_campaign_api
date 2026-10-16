from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.models.pilot import PilotModel
from app.db.models.user import UserModel
from app.dependencies.auth import get_current_user
from app.schemas.pilot import NamedPilot, PilotUpgradeRequest
from app.services.pilot_service import PilotService

router = APIRouter()


@router.get("/{pilot_id}", response_model=NamedPilot, summary="Информация о пилоте")
async def get_pilot(
    pilot_id: str = Path(..., description="UUID пилота"),
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Возвращает карточку пилота из СУБД."""
    stmt = select(PilotModel).where(PilotModel.id == pilot_id)
    res = await db.execute(stmt)
    pilot = res.scalar_one_or_none()
    if not pilot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пилот не найден")
    return pilot


@router.post("/{pilot_id}/upgrade", response_model=NamedPilot, summary="Прокачка пилота за XP")
async def upgrade_pilot(
    request: PilotUpgradeRequest,
    pilot_id: str = Path(..., description="UUID пилота"),
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Транзакционно улучшает навык Gunnery/Piloting, добавляет Edge или покупает SPA за XP.
    
    * **400 Bad Request**: Недостаточно XP (`InsufficientXPError`) или достигнут предел.
    """
    stmt = select(PilotModel).where(PilotModel.id == pilot_id)
    res = await db.execute(stmt)
    pilot = res.scalar_one_or_none()
    if not pilot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пилот не найден")

    try:
        return await PilotService.upgrade_pilot(db=db, pilot=pilot, request=request)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))