from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import InsufficientSupportPointsError
from app.db.models.force import ForceModel, MechUnitModel
from app.db.models.pilot import PilotModel
from app.schemas.force import UnitStatus
from app.schemas.track import TrackCompletionRequest, TrackCompletionResponse, XPAllocationResult


class TrackService:
    @staticmethod
    async def start_track(db: AsyncSession, force: ForceModel, entry_cost_sp: int) -> ForceModel:
        if force.support_points < entry_cost_sp:
            raise InsufficientSupportPointsError(required=entry_cost_sp, available=force.support_points)
        force.support_points -= entry_cost_sp
        db.add(force)
        await db.flush()
        return force

    @staticmethod
    async def complete_track(
        db: AsyncSession,
        force: ForceModel,
        track_id: str,
        earned_sp: int,
        request: TrackCompletionRequest
    ) -> TrackCompletionResponse:
        total_sp_spent = sum(p.sp_allocated_to_xp for p in request.pilot_performances)
        net_sp = earned_sp - total_sp_spent
        
        force.support_points += net_sp
        db.add(force)

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

        if request.damaged_unit_ids:
            await TrackService._update_units_status(db, request.damaged_unit_ids, UnitStatus.DAMAGED)
        if request.destroyed_unit_ids:
            await TrackService._update_units_status(db, request.destroyed_unit_ids, UnitStatus.DESTROYED)
        if request.truly_destroyed_unit_ids:
            await TrackService._update_units_status(db, request.truly_destroyed_unit_ids, UnitStatus.TRULY_DESTROYED)

        await db.flush()

        return TrackCompletionResponse(
            track_id=track_id,
            sp_earned=earned_sp,
            total_sp_spent_on_xp=total_sp_spent,
            net_sp_gained=net_sp,
            xp_allocations=xp_results,
            summary=f"Трек '{track_id}' завершен. Заработано: {earned_sp} SP. Списано на XP: {total_sp_spent} SP. Чистый прирост: {net_sp} SP."
        )

    @staticmethod
    async def _update_units_status(db: AsyncSession, unit_ids: List[str], status: UnitStatus) -> None:
        stmt = select(MechUnitModel).where(MechUnitModel.id.in_(unit_ids))
        res = await db.execute(stmt)
        for unit in res.scalars():
            unit.status = status
            db.add(unit)