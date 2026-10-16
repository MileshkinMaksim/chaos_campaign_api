import random
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.models.force import ForceModel
from app.dependencies.campaign import verify_force_ownership
from app.schemas.force import Faction, WeightClass
from app.schemas.logistics import PurchaseUnitRequest, RepairRequest, ScrapUnitRequest
from app.services.logistics_service import LogisticsService

router = APIRouter()


@router.post("/repair", summary="Ремонт техники за SP")
async def repair_unit(
    request: RepairRequest,
    sp_cost: int = Query(50, ge=0),
    force_id: str = Query(...),
    force: ForceModel = Depends(verify_force_ownership),
    db: AsyncSession = Depends(get_db)
):
    """Восстанавливает поврежденный мех до статуса OPERATIONAL за SP."""
    try:
        repaired_unit = await LogisticsService.repair_unit(
            db=db, force=force, unit_id=request.unit_id, sp_cost=sp_cost
        )
        return {"status": "repaired", "unit_id": repaired_unit.id, "remaining_sp": force.support_points}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/scrap", summary="Утилизация уничтоженной техники на лом")
async def scrap_unit(
    request: ScrapUnitRequest,
    force_id: str = Query(...),
    force: ForceModel = Depends(verify_force_ownership),
    db: AsyncSession = Depends(get_db)
):
    """Списывает полностью уничтоженный мех (TRULY_DESTROYED) и зачисляет 25% стоимости в SP."""
    try:
        sp_yield = await LogisticsService.scrap_unit(db=db, force=force, unit_id=request.unit_id)
        return {"status": "scrapped", "sp_earned": sp_yield, "total_sp": force.support_points}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/buy-unit", summary="Покупка новой техники")
async def buy_unit(
    request: PurchaseUnitRequest,
    force_id: str = Query(...),
    force: ForceModel = Depends(verify_force_ownership),
    db: AsyncSession = Depends(get_db)
):
    """Приобретает новый мех и привязывает его к ростеру отряда."""
    try:
        new_unit = await LogisticsService.buy_unit(db=db, force=force, request=request)
        return {"status": "purchased", "unit": new_unit, "remaining_sp": force.support_points}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/rat-roll", summary="Ролл по таблицам RAT (Random Assignment Tables)")
async def rat_roll(
    faction: Faction = Query(...),
    weight_class: WeightClass = Query(...),
    unit_rating: str = Query("Scale 1", pattern=r"^Scale [1-3]$")
):
    """Генерирует случайный мех по таблицам RAT региона Draconis Reach."""
    sample_mechs = {
        WeightClass.LIGHT: [("Panther", "PTH-9R"), ("Jenner", "JR7-D"), ("Locust", "LCT-1E")],
        WeightClass.MEDIUM: [("Starslayer", "STAGE-3C"), ("Phoenix Hawk", "PXH-1K"), ("Centurion", "CN9-A")],
        WeightClass.HEAVY: [("Dragon", "DRG-1N"), ("Catapult", "CPLT-C1"), ("Grasshopper", "GHR-5H")],
        WeightClass.ASSAULT: [("Awesome", "AWS-8Q"), ("BattleMaster", "BLR-1D"), ("Stalker", "STK-3H")],
    }
    chassis, model = random.choice(sample_mechs[weight_class])
    return {
        "faction": faction,
        "weight_class": weight_class,
        "unit_rating": unit_rating,
        "rolled_mech": {"chassis": chassis, "model": model}
    }