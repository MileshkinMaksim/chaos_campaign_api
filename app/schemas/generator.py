from typing import Optional
from pydantic import BaseModel, Field
from app.schemas.force import Faction


class ContractGenerateRequest(BaseModel):
    """Параметры процедуры генерации случайного контракта."""
    employer: Optional[Faction] = Field(None, description="Целевой наниматель")
    target_faction: Optional[Faction] = Field(None, description="Вражеская фракция")
    location_hot_spot: Optional[str] = Field(None, description="Локация в Draconis Reach")