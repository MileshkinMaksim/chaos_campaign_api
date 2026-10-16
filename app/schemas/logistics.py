from pydantic import BaseModel, Field
from app.schemas.force import Faction, WeightClass


class RepairRequest(BaseModel):
    """Запрос на ремонт поврежденной техники за SP."""
    unit_id: str = Field(..., description="ID поврежденного меха")


class ScrapUnitRequest(BaseModel):
    """Запрос на утилизацию уничтоженной техники (TRULY_DESTROYED) на лом."""
    unit_id: str = Field(..., description="ID техники для утилизации в SP в БД")


class PurchaseUnitRequest(BaseModel):
    """Запрос на покупку новой единицы техники."""
    chassis: str = Field(..., json_schema_extra={"example": "Catapult"})
    model: str = Field(..., json_schema_extra={"example": "CPLT-C1"})
    tonnage: int = Field(..., ge=20, le=100, json_schema_extra={"example": 65})
    weight_class: WeightClass = Field(..., json_schema_extra={"example": WeightClass.HEAVY})
    bv2: int = Field(..., ge=100, le=5000, json_schema_extra={"example": 1399})
    cost_sp: int = Field(..., ge=0, json_schema_extra={"example": 300})


class RATRollQuery(BaseModel):
    """Параметры генерации случайной техники по RAT-таблицам."""
    faction: Faction
    unit_rating: str = Field(..., pattern=r"^Scale [1-3]$", description="Рейтинг подразделения (Scale 1, Scale 2, Scale 3)")
    weight_class: WeightClass