from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.models.force import ForceModel
from app.db.models.user import UserModel
from app.dependencies.auth import get_current_user
from app.dependencies.campaign import verify_force_ownership
from app.schemas.contract import ContractNegotiationOffer, ContractResponse
from app.schemas.force import Faction
from app.services.generator_service import GeneratorService
from app.services.negotiation_engine import NegotiationEngine

router = APIRouter()


@router.get("/available", response_model=List[ContractResponse], summary="Поиск доступных контрактов")
async def get_available_contracts(
    employer: Optional[Faction] = Query(None, description="Фильтр по нанимателю"),
    location: Optional[str] = Query(None, min_length=2, description="Локация Hot Spot"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=50),
    current_user: UserModel = Depends(get_current_user)
):
    """Возвращает список доступных контрактов с поддержкой фильтрации и пагинации."""
    # Генерация примеров контрактов для каталога
    contracts = [
        GeneratorService.generate_random_contract(
            employer=employer or Faction.DRACONIS_COMBINE,
            target_faction=Faction.FEDERATED_SUNS
        ) for _ in range(limit)
    ]
    return contracts


@router.post("/{contract_id}/negotiate", summary="Переговоры по условиям контракта")
async def negotiate_contract(
    contract_id: str,
    offer: ContractNegotiationOffer,
    force_id: str = Query(..., description="ID отряда"),
    force: ForceModel = Depends(verify_force_ownership)
):
    """
    Проверяет запрашиваемые условия контракта с Очками Репутации отряда.
    
    * **400 Bad Request**: Недостаточно репутации (`ReputationRequirementNotMetError`).
    """
    mock_contract = GeneratorService.generate_random_contract()
    mock_contract.id = contract_id

    NegotiationEngine.validate_negotiation_offer(
        force=force, contract=mock_contract, requested_terms=offer.requested_terms
    )
    mock_contract.terms = offer.requested_terms
    return {"status": "terms_accepted", "contract": mock_contract}


@router.post("/{contract_id}/sign", summary="Подписание контракта")
async def sign_contract(
    contract_id: str,
    force_id: str = Query(...),
    force: ForceModel = Depends(verify_force_ownership)
):
    """Подписывает контракт и закрепляет его за отрядом."""
    return {"status": "contract_signed", "contract_id": contract_id, "force_id": force.id}