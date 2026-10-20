import json
from typing import Any, Dict, List
from fastapi import APIRouter, Depends, File, Form, HTTPException, Path, UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.database import get_db
from app.db.models.force import ForceModel, MechUnitModel
from app.db.models.pilot import PilotModel
from app.db.models.user import UserModel
from app.dependencies.auth import get_current_user
from app.dependencies.campaign import verify_force_ownership
from app.schemas.force import AssignPilotRequest, ForceCreate, ForceResponse
from app.services.force_service import ForceService
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.get("/starting-options", response_model=Dict[str, Any], summary="Получение стартовых опций для создания отряда")
async def get_starting_options():
    """Возвращает список доступных фракций с их описанием и RAT-мехами."""
    default_mechs = [
        {"chassis": "Flea", "model": "FLE-17", "weight_class": "Light", "tonnage": 20, "bv2": 510},
        {"chassis": "Flea", "model": "FLE-21", "weight_class": "Light", "tonnage": 20, "bv2": 826},
        {"chassis": "Chameleon", "model": "CLN-7V", "weight_class": "Medium", "tonnage": 50, "bv2": 1042},
        {"chassis": "Quickdraw", "model": "QKD-5M", "weight_class": "Heavy", "tonnage": 60, "bv2": 1237},
        {"chassis": "Ostsol", "model": "OTL-5M", "weight_class": "Heavy", "tonnage": 60, "bv2": 1245},
        {"chassis": "Chameleon", "model": "CLN-8V", "weight_class": "Medium", "tonnage": 50, "bv2": 1426},
        {"chassis": "Starslayer", "model": "STY-3C", "weight_class": "Medium", "tonnage": 50, "bv2": 1508},
        {"chassis": "Ostsol", "model": "OTL-8E", "weight_class": "Heavy", "tonnage": 60, "bv2": 1552},
        {"chassis": "Caesar", "model": "CES-3R", "weight_class": "Heavy", "tonnage": 70, "bv2": 1578},
        {"chassis": "Caesar", "model": "CES-5R", "weight_class": "Heavy", "tonnage": 70, "bv2": 2192},
        {"chassis": "Starslayer", "model": "STY-4C", "weight_class": "Medium", "tonnage": 50, "bv2": 2218},
        {"chassis": "Quickdraw", "model": "QKD-9G", "weight_class": "Heavy", "tonnage": 60, "bv2": 2224},
        {"chassis": "Devastator", "model": "DVS-2", "weight_class": "Assault", "tonnage": 100, "bv2": 2481},
    ]

    return {
        "available_factions": [
            {
                "faction": "Draconis Combine",
                "display_name": "Draconis Combine",
                "description": "Синдикат Дракона",
                "available_rat_mechs": default_mechs
            },
            {
                "faction": "Federated Suns",
                "display_name": "Federated Suns",
                "description": "Федеративные Солнца",
                "available_rat_mechs": default_mechs
            },
            {
                "faction": "Raven Alliance",
                "display_name": "Raven Alliance",
                "description": "Вороний Альянс",
                "available_rat_mechs": default_mechs
            },
            {
                "faction": "Clan Sea Fox",
                "display_name": "Clan Sea Fox",
                "description": "Клан Морских Лис",
                "available_rat_mechs": default_mechs
            },
            {
                "faction": "Republic of the Sphere",
                "display_name": "Republic of the Sphere",
                "description": "Республика Сферы",
                "available_rat_mechs": default_mechs
            },
            {
                "faction": "Mercenary",
                "display_name": "Mercenary",
                "description": "Независимые наемники",
                "available_rat_mechs": default_mechs
            }
        ],
        "max_starting_mechs": 2,
        "max_starting_bv2": 3000,
        "starting_sp": 3000,
        "starting_reputation": 1,
        "starting_pilots_count": 2,
        "starting_xp_per_pilot": 150
    }


@router.get("/me", response_model=List[ForceResponse], summary="Получение всех отрядов текущего пользователя")
async def get_my_forces(
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Возвращает список всех отрядов авторизованного пользователя."""
    stmt = (
        select(ForceModel)
        .where(ForceModel.owner_id == current_user.id)
        .options(selectinload(ForceModel.units), selectinload(ForceModel.pilots))
        .order_by(ForceModel.id.desc())
    )
    result = await db.execute(stmt)
    forces = result.scalars().all()

    if not forces:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="У текущего пользователя еще нет созданного отряда"
        )
    return forces


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

@router.delete("/{force_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удаление отряда")
async def delete_force(
    force_id: str = Path(..., min_length=3),
    force: ForceModel = Depends(verify_force_ownership),
    db: AsyncSession = Depends(get_db)
):
    """Каскадно удаляет отряд пользователя со всей связанной техникой и пилотами."""
    await ForceService.delete_force(db=db, force=force)
    return None

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
        "sponsoring_faction": force.sponsoring_faction,
        "warchest_sp": force.support_points,
        "reputation_score": force.reputation_score,
        "total_units_count": len(force.units),
        "total_pilots_count": len(force.pilots),
        "roster": [
            {
                "id": u.id,
                "chassis": u.chassis,
                "model": u.model,
                "tonnage": u.tonnage,
                "weight_class": u.weight_class,
                "bv2": u.bv2,
                "status": u.status,
                "assigned_pilot_id": u.assigned_pilot_id
            } for u in force.units
        ],
        "pilots": [
            {
                "id": p.id,
                "name": p.name,
                "gunnery": p.gunnery,
                "piloting": p.piloting,
                "experience_points": p.experience_points,
                "edge_points": p.edge_points
            } for p in force.pilots
        ]
    }
    return JSONResponse(
        content=jsonable_encoder(record_sheet),
        headers={"Content-Disposition": f"attachment; filename={force.name}_record_sheet.json"}
    )

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