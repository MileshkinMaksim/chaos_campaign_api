from typing import Annotated, List, Literal, Union, Optional
from pydantic import BaseModel, Field, ConfigDict


class NamedPilot(BaseModel):
    """Модель именного пилота отряда наемников."""
    id: str = Field(..., description="Уникальный UUID пилота в БД")
    force_id: Optional[str] = Field(None, description="ID отряда в БД")
    name: str = Field(..., min_length=2, max_length=50, json_schema_extra={"example": "Maverick Banderas"})
    gunnery: int = Field(default=4, ge=0, le=8, description="Навык стрельбы (чем ниже, тем лучше)")
    piloting: int = Field(default=5, ge=0, le=8, description="Навык пилотирования (чем ниже, тем лучше)")
    
    # Система опыта (XP)
    experience_points: int = Field(default=0, ge=0, description="Доступные очки опыта (XP)")
    total_xp_earned: int = Field(default=0, ge=0, description="Всего заработано XP за кампанию")
    
    # Способности и Edge
    edge_points: int = Field(default=1, ge=0, le=10, description="Текущее значение Edge (0-10)")
    special_abilities: List[str] = Field(
        default_factory=list, 
        json_schema_extra={"example": ["Overcharge", "Dodge", "Marksman"]},
        description="Купленные спец-способности (SPAs) и способности Edge"
    )
    is_temporary_hire: bool = Field(default=False)

    model_config = ConfigDict(from_attributes=True)


# --- Discriminated Unions для полиморфных запросов на улучшение пилота ---

class SkillUpgrade(BaseModel):
    """Улучшение навыка стрельбы или пилотирования."""
    upgrade_type: Literal["gunnery", "piloting"]


class EdgeUpgrade(BaseModel):
    """Покупка дополнительного очка Edge."""
    upgrade_type: Literal["edge"]


class AbilityUpgrade(BaseModel):
    """Покупка специальной способности (SPA)."""
    upgrade_type: Literal["ability"]
    ability_name: str = Field(..., min_length=2, description="Название спец-способности (SPA)")


PilotUpgradeRequest = Annotated[
    Union[SkillUpgrade, EdgeUpgrade, AbilityUpgrade], 
    Field(discriminator="upgrade_type")
]