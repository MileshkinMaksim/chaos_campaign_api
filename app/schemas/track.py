from typing import List
from pydantic import BaseModel, Field, model_validator


class PilotTrackPerformance(BaseModel):
    pilot_id: str
    survived: bool = True
    objectives_completed: int = Field(default=0, ge=0)
    kills: int = Field(default=0, ge=0)
    is_mvp: bool = Field(default=False)
    sp_allocated_to_xp: int = Field(default=0, ge=0, le=100)


class TrackCompletionRequest(BaseModel):
    completed_objectives_ids: List[str]
    pilot_performances: List[PilotTrackPerformance]
    damaged_unit_ids: List[str] = []
    destroyed_unit_ids: List[str] = []
    truly_destroyed_unit_ids: List[str] = []

    @model_validator(mode="after")
    def validate_total_sp_conversion(self) -> "TrackCompletionRequest":
        total_sp = sum(p.sp_allocated_to_xp for p in self.pilot_performances)
        if total_sp > 200:
            raise ValueError(f"Суммарная конвертация SP в XP за трек не может превышать 200 SP (запрошено: {total_sp} SP)")
        return self


class XPAllocationResult(BaseModel):
    pilot_id: str
    pilot_name: str
    sp_converted_xp: int
    mvp_bonus_xp: int
    total_xp_gained: int
    new_total_xp: int


class TrackCompletionResponse(BaseModel):
    track_id: str
    sp_earned: int
    total_sp_spent_on_xp: int
    net_sp_gained: int
    xp_allocations: List[XPAllocationResult]
    summary: str