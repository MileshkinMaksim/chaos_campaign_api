from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.force import ForceModel, MechUnitModel
from app.db.models.pilot import PilotModel
from app.schemas.force import ForceCreate


class ForceService:
    @staticmethod
    async def create_force(
        db: AsyncSession, 
        owner_id: str, 
        force_in: ForceCreate
    ) -> ForceModel:
        """Создает новый отряд наемников с начальным балансом WP=1000, SP=500, Rep=10."""
        new_force = ForceModel(
            owner_id=owner_id,
            name=force_in.name,
            sponsoring_faction=force_in.sponsoring_faction,
            warchest_points=1000,
            support_points=500,
            reputation_score=10,
        )
        db.add(new_force)
        await db.flush()
        return new_force

    @staticmethod
    async def assign_pilot_to_unit(
        db: AsyncSession,
        force: ForceModel,
        unit_id: str,
        pilot_id: Optional[str]
    ) -> ForceModel:
        """Назначает или снимает (pilot_id=None) пилота с боевой машины."""
        stmt = select(MechUnitModel).where(
            MechUnitModel.id == unit_id, 
            MechUnitModel.force_id == force.id
        )
        result = await db.execute(stmt)
        unit = result.scalar_one_or_none()
        
        if not unit:
            raise ValueError(f"Мех с ID {unit_id} не найден в данном отряде")

        if pilot_id is not None:
            pilot_stmt = select(PilotModel).where(
                PilotModel.id == pilot_id, 
                PilotModel.force_id == force.id
            )
            pilot_result = await db.execute(pilot_stmt)
            pilot = pilot_result.scalar_one_or_none()
            if not pilot:
                raise ValueError(f"Пилот с ID {pilot_id} не найден в данном отряде")

        unit.assigned_pilot_id = pilot_id
        db.add(unit)
        await db.flush()
        return force