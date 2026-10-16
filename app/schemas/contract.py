from enum import Enum
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.force import Faction


class CommandRights(str, Enum):
    INTEGRATED = "Integrated"
    CO_COMMAND = "Co-Command"
    INDEPENDENT = "Independent"


class SalvageRights(str, Enum):
    FULL = "Full"
    SHARED = "Shared"
    EXCHANGE = "Exchange"
    NONE = "None"


class ContractTerms(BaseModel):
    """Условия контракта."""
    base_payment_wp: int = Field(..., ge=0, json_schema_extra={"example": 500})
    overhead_sp: int = Field(..., ge=0, json_schema_extra={"example": 200})
    command_rights: CommandRights = Field(default=CommandRights.INDEPENDENT)
    salvage_rights: SalvageRights = Field(default=SalvageRights.SHARED)
    support_rights_percent: int = Field(default=50, ge=0, le=100)
    transport_coverage_percent: int = Field(default=100, ge=0, le=100, description="Покрытие транспортных расходов")

    model_config = ConfigDict(from_attributes=True)


class ContractNegotiationOffer(BaseModel):
    """Запрос на согласование новых условий."""
    requested_terms: ContractTerms


class ContractResponse(BaseModel):
    """Паспорт контракта из БД."""
    id: str
    title: str = Field(..., json_schema_extra={"example": "Raid on Palmyra"})
    employer: Faction
    target_faction: Faction
    location_hot_spot: str = Field(..., json_schema_extra={"example": "Palmyra"})
    required_reputation: int = Field(default=5, description="Минимальная Репутация для согласования условий")
    terms: ContractTerms
    is_signed: bool = False
    is_completed: bool = False

    model_config = ConfigDict(from_attributes=True)