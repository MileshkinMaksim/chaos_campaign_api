from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import InsufficientXPError
from app.db.models.pilot import PilotModel
from app.schemas.pilot import (
    AbilityUpgrade,
    EdgeUpgrade,
    PilotUpgradeRequest,
    SkillUpgrade,
)

# Нелинейные таблицы стоимости прокачки пилотов (в XP) согласно спецификации v3.0
GUNNERY_UPGRADE_COSTS = {4: 300, 3: 700, 2: 1200, 1: 2200}
PILOTING_UPGRADE_COSTS = {5: 100, 4: 200, 3: 700, 2: 1200}
EDGE_UPGRADE_COSTS = {
    1: 60, 2: 120, 3: 200, 4: 300, 5: 420,
    6: 560, 7: 720, 8: 900, 9: 1100
}
SPA_COST_TABLE = [60, 180, 360, 600, 900]


class PilotService:
    @staticmethod
    async def upgrade_pilot(
        db: AsyncSession, 
        pilot: PilotModel, 
        request: PilotUpgradeRequest
    ) -> PilotModel:
        """
        Прокачивает характеристики пилота за XP в рамках асинхронной транзакции БД.
        
        :raises InsufficientXPError: Если у пилота недостаточно experience_points.
        :raises ValueError: Если достигнут лимит развития параметра.
        """
        if isinstance(request, SkillUpgrade):
            if request.upgrade_type == "gunnery":
                cost = GUNNERY_UPGRADE_COSTS.get(pilot.gunnery)
                if cost is None:
                    raise ValueError("Достигнут максимальный навык Gunnery (0)")
                if pilot.experience_points < cost:
                    raise InsufficientXPError(required=cost, available=pilot.experience_points)
                pilot.experience_points -= cost
                pilot.gunnery -= 1

            elif request.upgrade_type == "piloting":
                cost = PILOTING_UPGRADE_COSTS.get(pilot.piloting)
                if cost is None:
                    raise ValueError("Достигнут максимальный навык Piloting (1)")
                if pilot.experience_points < cost:
                    raise InsufficientXPError(required=cost, available=pilot.experience_points)
                pilot.experience_points -= cost
                pilot.piloting -= 1

        elif isinstance(request, EdgeUpgrade):
            cost = EDGE_UPGRADE_COSTS.get(pilot.edge_points)
            if cost is None:
                raise ValueError("Достигнуто максимальное значение Edge (10)")
            if pilot.experience_points < cost:
                raise InsufficientXPError(required=cost, available=pilot.experience_points)
            pilot.experience_points -= cost
            pilot.edge_points += 1

        elif isinstance(request, AbilityUpgrade):
            # Расчет стоимости очередной спец-способности (SPA)
            current_abilities_count = len(getattr(pilot, "special_abilities", []))
            ability_index = min(current_abilities_count, len(SPA_COST_TABLE) - 1)
            cost = SPA_COST_TABLE[ability_index]
            
            if pilot.experience_points < cost:
                raise InsufficientXPError(required=cost, available=pilot.experience_points)
            
            pilot.experience_points -= cost
            # Примечание: подробный список спец-способностей сохраняется в связных таблицах или JSON
            
        db.add(pilot)
        await db.flush()
        return pilot