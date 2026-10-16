from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import InsufficientWarchestPointsError
from app.db.models.force import ForceModel, MechUnitModel
from app.db.models.pilot import PilotModel
from app.schemas.force import UnitStatus
from app.schemas.track import (
    TrackCompletionRequest,
    TrackCompletionResponse,
    XPAllocationResult,
)


class TrackService:
    @staticmethod
    async def start_track(
        db: AsyncSession, 
        force: ForceModel, 
        entry_cost_wp: int
    ) -> ForceModel:
        """Списывает стоимость входа в миссию (Warchest Entry Cost)."""
        if force.warchest_points < entry_cost_wp:
            raise InsufficientWarchestPointsError(
                required=entry_cost_wp, 
                available=force.warchest_points
            )
        force.warchest_points -= entry_cost_wp
        db.add(force)
        await db.flush()
        return force

    @staticmethod
    async def complete_track(
        db: AsyncSession,
        force: ForceModel,
        track_id: str,
        earned_wp: int,
        earned_sp: int,
        request: TrackCompletionRequest
    ) -> TrackCompletionResponse:
        """Транзакционная фиксация итогов миссии и попилотная конвертация SP -> XP."""
        # 1. Расчет конвертации SP в XP
        total_sp_spent = sum(p.sp_allocated_to_xp for p in request.pilot_performances)
        
        # Зачисление сетевого прироста ресурсов
        force.warchest_points += earned_wp
        force.support_points += (earned_sp - total_sp_spent)
        db.add(force)

        # 2. Начисление XP пилотам
        xp_results: List[XPAllocationResult] = []
        for perf in request.pilot_performances:
            pilot_stmt = select(PilotModel).where(PilotModel.id == perf.pilot_id)
            pilot_res = await db.execute(pilot_stmt)
            pilot = pilot_res.scalar_one_or_none()
            
            if pilot:
                sp_xp = perf.sp_allocated_to_xp
                mvp_xp = 50 if perf.is_mvp else 0
                gained_xp = sp_xp + mvp_xp
                
                pilot.experience_points += gained_xp
                pilot.total_xp_earned += gained_xp
                db.add(pilot)

                xp_results.append(
                    XPAllocationResult(
                        pilot_id=pilot.id,
                        pilot_name=pilot.name,
                        sp_converted_xp=sp_xp,
                        mvp_bonus_xp=mvp_xp,
                        total_xp_gained=gained_xp,
                        new_total_xp=pilot.experience_points,
                    )
                )

        # 3. Фиксация повреждений техники
        if request.damaged_unit_ids:
            await TrackService._update_units_status(db, request.damaged_unit_ids, UnitStatus.DAMAGED)
        if request.destroyed_unit_ids:
            await TrackService._update_units_status(db, request.destroyed_unit_ids, UnitStatus.DESTROYED)
        if request.truly_destroyed_unit_ids:
            await TrackService._update_units_status(db, request.truly_destroyed_unit_ids, UnitStatus.TRULY_DESTROYED)

        await db.flush()

        return TrackCompletionResponse(
            track_id=track_id,
            wp_earned=earned_wp,
            sp_earned=earned_sp,
            total_sp_spent_on_xp=total_sp_spent,
            xp_allocations=xp_results,
            summary=f"Трек '{track_id}' завершен. Заработано: {earned_wp} WP, {earned_sp} SP. Списано на XP: {total_sp_spent} SP."
        )

    @staticmethod
    async def _update_units_status(db: AsyncSession, unit_ids: List[str], status: UnitStatus) -> None:
        stmt = select(MechUnitModel).where(MechUnitModel.id.in_(unit_ids))
        res = await db.execute(stmt)
        for unit in res.scalars():
            unit.status = status
            db.add(unit)