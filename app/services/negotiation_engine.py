from app.db.models.force import ForceModel
from app.schemas.contract import ContractResponse, ContractTerms
from app.core.exceptions import ReputationRequirementNotMetError


class NegotiationEngine:
    @staticmethod
    def validate_negotiation_offer(
        force: ForceModel,
        contract: ContractResponse,
        requested_terms: ContractTerms
    ) -> bool:
        """Сравнивает текущий рейтинг репутации отряда с требуемым уровнем контракта."""
        if force.reputation_score < contract.required_reputation:
            raise ReputationRequirementNotMetError(
                required=contract.required_reputation,
                current=force.reputation_score
            )
        return True