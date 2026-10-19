from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict, model_validator
from app.schemas.pilot import NamedPilot


class Faction(str, Enum):
    DRACONIS_COMBINE = "Draconis Combine"
    FEDERATED_SUNS = "Federated Suns"
    RAVEN_ALLIANCE = "Raven Alliance"
    CLAN_SEA_FOX = "Clan Sea Fox"
    REPUBLIC_OF_THE_SPHERE = "Republic of the Sphere"
    MERCENARY = "Mercenary"


class UnitStatus(str, Enum):
    OPERATIONAL = "Operational"
    DAMAGED = "Damaged"
    DESTROYED = "Destroyed"
    TRULY_DESTROYED = "Truly Destroyed"


class WeightClass(str, Enum):
    LIGHT = "Light"
    MEDIUM = "Medium"
    HEAVY = "Heavy"
    ASSAULT = "Assault"


class MechUnit(BaseModel):
    id: str
    force_id: Optional[str] = None
    chassis: str
    model: str
    tonnage: int
    weight_class: WeightClass
    bv2: int
    status: UnitStatus = UnitStatus.OPERATIONAL
    assigned_pilot_id: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class StartingMechSelection(BaseModel):
    chassis: str
    model: str
    tonnage: int
    weight_class: WeightClass
    bv2: int


class ForceCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    sponsoring_faction: Faction
    starting_pilot_names: List[str] = Field(
        default_factory=lambda: ["Pilot Alpha", "Pilot Bravo"], 
        min_length=2, 
        max_length=2
    )
    selected_mechs: List[StartingMechSelection] = Field(..., min_length=1, max_length=2)

    @model_validator(mode="after")
    def validate_starting_force_rules(self) -> "ForceCreate":
        total_bv = sum(m.bv2 for m in self.selected_mechs)
        if total_bv > 3000:
            raise ValueError(f"Суммарный BV2 выбранных мехов ({total_bv}) превышает максимальный лимит 3000 BV2")
        return self


class ForceResponse(BaseModel):
    id: str
    owner_id: str
    name: str
    sponsoring_faction: Faction
    support_points: int = 3000
    reputation_score: int = 1
    units: List[MechUnit] = []
    pilots: List[NamedPilot] = []

    model_config = ConfigDict(from_attributes=True)


class AssignPilotRequest(BaseModel):
    unit_id: str = Field(..., description="ID меха")
    pilot_id: Optional[str] = Field(None, description="ID пилота (None если снять пилота)")


class StartingFactionOption(BaseModel):
    faction: Faction
    display_name: str
    description: str
    available_rat_mechs: List[StartingMechSelection]


class StartingOptionsResponse(BaseModel):
    available_factions: List[StartingFactionOption]
    max_starting_mechs: int = 2
    max_starting_bv2: int = 3000
    starting_sp: int = 3000
    starting_reputation: int = 1
    starting_pilots_count: int = 2
    starting_xp_per_pilot: int = 150