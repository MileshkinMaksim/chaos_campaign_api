from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.force import ForceModel, MechUnitModel
from app.schemas.force import UnitStatus
from app.schemas.logistics import PurchaseUnitRequest


class LogisticsService:
    @staticmethod
    async def repair_unit(db: AsyncSession, force: ForceModel, unit_id: str, sp_cost: int) -> MechUnitModel:
        """Ремонтирует поврежденный мех за SP, возвращая ему статус OPERATIONAL."""
        if force.support_points < sp_cost:
            raise ValueError(f"Недостаточно SP для ремонта. Требуется: {sp_cost}, доступно: {force.support_points}")

        stmt = select(MechUnitModel).where(MechUnitModel.id == unit_id, MechUnitModel.force_id == force.id)
        res = await db.execute(stmt)
        unit = res.scalar_one_or_none()

        if not unit:
            raise ValueError("Техника не найдена в отряде")

        force.support_points -= sp_cost
        unit.status = UnitStatus.OPERATIONAL
        db.add_all([force, unit])
        await db.flush()
        return unit

    @staticmethod
    async def scrap_unit(db: AsyncSession, force: ForceModel, unit_id: str) -> int:
        """
        Утилизирует уничтоженный мех (TRULY_DESTROYED) на лом.
        Зачисляет 25% его базовой стоимости в SP и удаляет объект из БД.
        """
        stmt = select(MechUnitModel).where(MechUnitModel.id == unit_id, MechUnitModel.force_id == force.id)
        res = await db.execute(stmt)
        unit = res.scalar_one_or_none()

        if not unit:
            raise ValueError("Техника не найдена в отряде")
        if unit.status != UnitStatus.TRULY_DESTROYED:
            raise ValueError("На лом можно распилить только полностью уничтоженную технику (TRULY_DESTROYED)")

        # Расчет 25% стоимости от тоннажа/BV2 в SP
        sp_yield = int((unit.tonnage * 10) * 0.25)
        force.support_points += sp_yield

        await db.delete(unit)
        db.add(force)
        await db.flush()
        return sp_yield

    @staticmethod
    async def buy_unit(db: AsyncSession, force: ForceModel, request: PurchaseUnitRequest) -> MechUnitModel:
        """Покупка новой техники за SP."""
        if force.support_points < request.cost_sp:
            raise ValueError(f"Недостаточно SP для покупки. Требуется: {request.cost_sp}, доступно: {force.support_points}")

        force.support_points -= request.cost_sp
        new_unit = MechUnitModel(
            force_id=force.id,
            chassis=request.chassis,
            model=request.model,
            tonnage=request.tonnage,
            weight_class=request.weight_class,
            bv2=request.bv2,
            status=UnitStatus.OPERATIONAL
        )
        db.add_all([force, new_unit])
        await db.flush()
        return new_unit