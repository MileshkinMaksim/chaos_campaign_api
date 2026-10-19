import random
from app.schemas.contract import ContractResponse, ContractTerms, CommandRights, SalvageRights
from app.schemas.force import Faction

HOT_SPOTS = ["Alshain", "Buckminster", "Luthien", "Pesht", "Misery"]


class GeneratorService:
    @staticmethod
    def generate_random_contract(
        employer: Faction = Faction.DRACONIS_COMBINE,
        target_faction: Faction = Faction.FEDERATED_SUNS
    ) -> ContractResponse:
        """Процедурная генерация случайного контракта в SP."""
        location = random.choice(HOT_SPOTS)
        base_sp = random.randint(3, 8) * 100
        overhead_sp = random.randint(2, 5) * 100
        req_rep = random.randint(1, 5)

        terms = ContractTerms(
            base_payment_sp=base_sp,
            overhead_sp=overhead_sp,
            command_rights=random.choice(list(CommandRights)),
            salvage_rights=random.choice(list(SalvageRights)),
            support_rights_percent=50,
            transport_coverage_percent=100
        )

        return ContractResponse(
            id="generated-contract-001",
            title=f"Operation at {location}",
            employer=employer,
            target_faction=target_faction,
            location_hot_spot=location,
            required_reputation=req_rep,
            terms=terms,
            is_signed=False,
            is_completed=False
        )