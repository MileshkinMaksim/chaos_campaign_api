import json
from typing import List
from fastapi import APIRouter, Depends, File, Form, HTTPException, Path, UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.models.force import ForceModel, MechUnitModel
from app.db.models.pilot import PilotModel
from app.db.models.user import UserModel
from app.dependencies.auth import get_current_user
from app.dependencies.campaign import verify_force_ownership
from app.schemas.force import AssignPilotRequest, ForceCreate, ForceResponse
from app.services.force_service import ForceService

router = APIRouter()


@router.post("/", response_model=ForceResponse, status_code=status.HTTP_201_CREATED, summary="Создание нового отряда")
async def create_force(
    force_in: ForceCreate,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Создает новый отряд наемников для авторизованного пользователя."""
    return await ForceService.create_force(db=db, owner_id=current_user.id, force_in=force_in)


@router.get("/{force_id}", response_model=ForceResponse, summary="Получение карточки отряда")
async def get_force(
    force_id: str = Path(..., min_length=3, description="UUID отряда"),
    force: ForceModel = Depends(verify_force_ownership)
):
    """Возвращает полную структуру отряда с подгруженными списками техники и пилотов."""
    return force


@router.post("/{force_id}/assign-pilot", response_model=ForceResponse, summary="Назначение пилота на мех")
async def assign_pilot(
    request: AssignPilotRequest,
    force_id: str = Path(..., min_length=3),
    force: ForceModel = Depends(verify_force_ownership),
    db: AsyncSession = Depends(get_db)
):
    """Назначает или снимает пилота с техники в СУБД."""
    try:
        return await ForceService.assign_pilot_to_unit(
            db=db, force=force, unit_id=request.unit_id, pilot_id=request.pilot_id
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{force_id}/export", summary="Экспорт Mercenary Force Record Sheet")
async def export_force_record_sheet(
    force_id: str = Path(..., min_length=3),
    force: ForceModel = Depends(verify_force_ownership)
):
    """Генерирует и возвращает официальный бланк отряда в формате JSON."""
    record_sheet = {
        "unit_name": force.name,
        "sponsoring_faction": force.sponsoring_faction.value,
        "warchest_points": force.warchest_points,
        "support_points": force.support_points,
        "reputation_score": force.reputation_score,
        "total_units_count": len(force.units),
        "total_pilots_count": len(force.pilots),
        "roster": [
            {
                "chassis": u.chassis,
                "model": u.model,
                "tonnage": u.tonnage,
                "bv2": u.bv2,
                "status": u.status.value,
                "assigned_pilot_id": u.assigned_pilot_id
            } for u in force.units
        ]
    }
    return JSONResponse(content=record_sheet, headers={"Content-Disposition": f"attachment; filename={force.name}_record_sheet.json"})


@router.post("/{force_id}/roster/import", response_model=ForceResponse, summary="Импорт ростера из JSON файла")
async def import_force_roster(
    file: UploadFile = File(...),
    force_id: str = Path(..., min_length=3),
    force: ForceModel = Depends(verify_force_ownership),
    db: AsyncSession = Depends(get_db)
):
    """Пакетно загружает список мехов и пилотов из загруженного файла."""
    content = await file.read()
    try:
        data = json.loads(content)
        for unit_data in data.get("units", []):
            unit = MechUnitModel(
                force_id=force.id,
                chassis=unit_data["chassis"],
                model=unit_data["model"],
                tonnage=unit_data["tonnage"],
                weight_class=unit_data["weight_class"],
                bv2=unit_data["bv2"]
            )
            db.add(unit)

        for pilot_data in data.get("pilots", []):
            pilot = PilotModel(
                force_id=force.id,
                name=pilot_data["name"],
                gunnery=pilot_data.get("gunnery", 4),
                piloting=pilot_data.get("piloting", 5)
            )
            db.add(pilot)

        await db.flush()
        return force
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Ошибка парсинга файла: {str(e)}")