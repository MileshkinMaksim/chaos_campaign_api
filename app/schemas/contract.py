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
    base_payment_sp: int = Field(..., ge=0, description="Базовая выплата в SP")
    overhead_sp: int = Field(..., ge=0, description="Операционные расходы в SP")
    command_rights: CommandRights = CommandRights.INDEPENDENT
    salvage_rights: SalvageRights = SalvageRights.SHARED
    support_rights_percent: int = Field(default=50, ge=0, le=100)
    transport_coverage_percent: int = Field(default=100, ge=0, le=100)

    model_config = ConfigDict(from_attributes=True)


class ContractNegotiationOffer(BaseModel):
    requested_terms: ContractTerms


class ContractResponse(BaseModel):
    id: str
    title: str
    employer: Faction
    target_faction: Faction
    location_hot_spot: str
    required_reputation: int = 1
    terms: ContractTerms
    is_signed: bool = False
    is_completed: bool = False

    model_config = ConfigDict(from_attributes=True)