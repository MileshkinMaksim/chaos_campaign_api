from fastapi import APIRouter, Depends
from app.schemas.contract import ContractResponse
from app.schemas.generator import ContractGenerateRequest
from app.services.generator_service import GeneratorService

router = APIRouter()


@router.post("/contract", response_model=ContractResponse, summary="Процедурная генерация контракта")
async def generate_contract(request: ContractGenerateRequest):
    """Создает случайный контракт по правилам книги Hot Spots."""
    return GeneratorService.generate_random_contract(
        employer=request.employer,
        target_faction=request.target_faction
    )