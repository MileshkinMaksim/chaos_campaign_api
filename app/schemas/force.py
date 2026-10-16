from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.pilot import NamedPilot


class Faction(str, Enum):
    DRACONIS_COMBINE = "Draconis Combine"
    FEDERATED_SUNS = "Federated Suns"
    RAVEN_ALLIANCE = "Raven Alliance"
    CLAN_SEA_FOX = "Clan Sea Fox"
    CAPELLAN_CONFEDERATION = "Capellan Confederation"
    MERCENARY = "Mercenary"


class UnitStatus(str, Enum):
    OPERATIONAL = "Operational"
    DAMAGED = "Damaged"
    DESTROYED = "Destroyed"           # Поврежден, подлежит дорогостоящему ремонту за SP
    TRULY_DESTROYED = "Truly Destroyed" # Полностью уничтожен, списан в лом (разбор на SP)


class WeightClass(str, Enum):
    LIGHT = "Light"
    MEDIUM = "Medium"
    HEAVY = "Heavy"
    ASSAULT = "Assault"


class MechUnit(BaseModel):
    """Единица боевой техники (Мех)."""
    id: str = Field(..., description="UUID единицы техники в БД")
    force_id: Optional[str] = Field(None, description="ID отряда в БД")
    chassis: str = Field(..., json_schema_extra={"example": "Starslayer"})
    model: str = Field(..., json_schema_extra={"example": "STAGE-3C"})
    tonnage: int = Field(..., ge=20, le=100, json_schema_extra={"example": 50})
    weight_class: WeightClass = Field(..., json_schema_extra={"example": WeightClass.MEDIUM})
    bv2: int = Field(..., ge=100, le=5000, json_schema_extra={"example": 1340})
    status: UnitStatus = Field(default=UnitStatus.OPERATIONAL)
    assigned_pilot_id: Optional[str] = Field(None, description="UUID назначенного пилота в БД")

    model_config = ConfigDict(from_attributes=True)


class ForceCreate(BaseModel):
    """Запрос на создание нового отряда."""
    name: str = Field(..., min_length=3, max_length=50, json_schema_extra={"example": "Rebel Girls"})
    sponsoring_faction: Faction = Field(default=Faction.MERCENARY)


class ForceResponse(BaseModel):
    """Карточка отряда наемников из БД."""
    id: str
    owner_id: str = Field(..., description="UUID пользователя-командира в БД")
    name: str = Field(..., json_schema_extra={"example": "Rebel Girls"})
    sponsoring_faction: Faction = Field(default=Faction.MERCENARY)
    warchest_points: int = Field(default=1000, description="Очки Warchest (WP)")
    support_points: int = Field(default=500, description="Очки снабжения (SP)")
    reputation_score: int = Field(default=10, description="Рейтинг репутации отряда (не сжигается)")
    units: List[MechUnit] = Field(default_factory=list)
    pilots: List[NamedPilot] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class AssignPilotRequest(BaseModel):
    """Запрос на назначение/снятие пилота с меха."""
    unit_id: str = Field(..., description="ID меха")
    pilot_id: Optional[str] = Field(None, description="ID пилота (None если снять пилота)")