from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.force import ForceModel, MechUnitModel
from app.db.models.pilot import PilotModel
from app.schemas.force import ForceCreate
from app.core.exceptions import InvalidStartingForceConfigError


class ForceService:
    @staticmethod
    async def create_force(db: AsyncSession, owner_id: str, force_in: ForceCreate) -> ForceModel:
        """Создает новый отряд по правилам спецификации v6.0."""
        if len(force_in.selected_mechs) > 2:
            raise InvalidStartingForceConfigError("Разрешено выбирать не более 2-х стартовых мехов")
        
        total_bv = sum(m.bv2 for m in force_in.selected_mechs)
        if total_bv > 3000:
            raise InvalidStartingForceConfigError(f"Превышен лимит 3000 BV2 (запрошено: {total_bv} BV2)")

        # 1. Инициализация отряда: SP=3000, Rep=1
        force = ForceModel(
            owner_id=owner_id,
            name=force_in.name,
            sponsoring_faction=force_in.sponsoring_faction,
            support_points=3000,
            reputation_score=1
        )
        db.add(force)
        await db.flush()

        # 2. Создание 2-х пилотов с 150 XP
        pilots = []
        for name in force_in.starting_pilot_names:
            pilot = PilotModel(
                force_id=force.id,
                name=name,
                gunnery=4,
                piloting=5,
                experience_points=150,
                total_xp_earned=150
            )
            db.add(pilot)
            pilots.append(pilot)
        await db.flush()

        # 3. Привязка выбранной техники
        for i, mech_data in enumerate(force_in.selected_mechs):
            assigned_pilot = pilots[i].id if i < len(pilots) else None
            unit = MechUnitModel(
                force_id=force.id,
                chassis=mech_data.chassis,
                model=mech_data.model,
                tonnage=mech_data.tonnage,
                weight_class=mech_data.weight_class,
                bv2=mech_data.bv2,
                assigned_pilot_id=assigned_pilot
            )
            db.add(unit)

        await db.commit()

        # 4. Запрос с eager loading связей для безопасной сериализации Pydantic
        stmt = (
            select(ForceModel)
            .where(ForceModel.id == force.id)
            .options(
                selectinload(ForceModel.pilots),
                selectinload(ForceModel.units)
            )
        )
        result = await db.execute(stmt)
        return result.scalar_one()

    create_starting_force = create_force

    @classmethod
    async def assign_pilot_to_unit(
        cls, db: AsyncSession, force: ForceModel, unit_id: str, pilot_id: str | None
    ) -> ForceModel:
        """Назначает или снимает пилота с техники."""
        unit = next((u for u in force.units if u.id == unit_id), None)
        if not unit:
            raise ValueError("Техника не найдена в составе этого отряда")

        if pilot_id:
            pilot = next((p for p in force.pilots if p.id == pilot_id), None)
            if not pilot:
                raise ValueError("Пилот не найден в составе этого отряда")
            unit.assigned_pilot_id = pilot.id
        else:
            unit.assigned_pilot_id = None

        await db.commit()
        await db.refresh(force)
        return force

    @classmethod
    async def delete_force(cls, db: AsyncSession, force: ForceModel) -> None:
        """Каскадно удаляет отряд и все связанные записи (юниты, пилоты)."""
        await db.delete(force)
        await db.commit()