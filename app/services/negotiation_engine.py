from app.core.exceptions import ReputationRequirementNotMetError
from app.db.models.force import ForceModel
from app.schemas.contract import ContractResponse, ContractTerms


class NegotiationEngine:
    @staticmethod
    def validate_negotiation_offer(
        force: ForceModel,
        contract: ContractResponse,
        requested_terms: ContractTerms
    ) -> bool:
        """
        Сравнивает текущий рейтинг репутации отряда с требуемым уровнем контракта.
        
        :raises ReputationRequirementNotMetError: Если статус репутации ниже требуемого.
        """
        if force.reputation_score < contract.required_reputation:
            raise ReputationRequirementNotMetError(
                required=contract.required_reputation,
                available=force.reputation_score
            )
        return True