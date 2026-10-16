from typing import List
from pydantic import BaseModel, Field, model_validator


class PilotTrackPerformance(BaseModel):
    """Результаты конкретного пилота за трек/миссию."""
    pilot_id: str
    survived: bool = True
    objectives_completed: int = Field(default=0, ge=0)
    kills: int = Field(default=0, ge=0)
    is_mvp: bool = Field(default=False, description="Признан лучшим пилотом миссии (+50 bonus XP)")
    sp_allocated_to_xp: int = Field(
        default=0, 
        ge=0, 
        le=100, 
        description="Количество SP, списанных с баланса трека и переведенных данному пилоту в XP (макс 100 SP на пилота)"
    )


class TrackCompletionRequest(BaseModel):
    """Запрос на фиксацию итогов выполненного трека."""
    completed_objectives_ids: List[str]
    pilot_performances: List[PilotTrackPerformance]
    damaged_unit_ids: List[str] = Field(default_factory=list)
    destroyed_unit_ids: List[str] = Field(default_factory=list)
    truly_destroyed_unit_ids: List[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_total_sp_conversion(self) -> "TrackCompletionRequest":
        """Проверка правила: суммарная конвертация SP в XP за трек не превышает 200 SP."""
        total_sp = sum(p.sp_allocated_to_xp for p in self.pilot_performances)
        if total_sp > 200:
            raise ValueError(
                f"Суммарная конвертация SP в XP за трек не может превышать 200 SP (запрошено: {total_sp} SP)"
            )
        return self


class XPAllocationResult(BaseModel):
    """Детализация начисленного опыта пилоту."""
    pilot_id: str
    pilot_name: str
    sp_converted_xp: int
    mvp_bonus_xp: int
    total_xp_gained: int
    new_total_xp: int


class TrackCompletionResponse(BaseModel):
    """Итоговый отчет о завершении трека."""
    track_id: str
    wp_earned: int
    sp_earned: int
    total_sp_spent_on_xp: int
    xp_allocations: List[XPAllocationResult]
    summary: str