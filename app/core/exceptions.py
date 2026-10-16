from fastapi import Request, status
from fastapi.responses import JSONResponse


class ChaosCampaignException(Exception):
    """Базовое исключение бизнес-логики Chaos Campaign."""
    def __init__(self, message: str, code: str):
        self.message = message
        self.code = code


class InsufficientXPError(ChaosCampaignException):
    """Исключение при нехватке очков опыта (XP) у пилота."""
    def __init__(self, required: int, available: int):
        super().__init__(
            message=f"Недостаточно опыта (XP). Требуется: {required}, доступно: {available}",
            code="INSUFFICIENT_XP"
        )


class ReputationRequirementNotMetError(ChaosCampaignException):
    """Исключение при несоответствии репутации отряда требованиям контракта."""
    def __init__(self, required: int, available: int):
        super().__init__(
            message=f"Недостаточно Репутации для согласования условий. Требуется: {required}, текущая: {available}",
            code="REPUTATION_REQUIREMENT_NOT_MET"
        )


class InsufficientWarchestPointsError(ChaosCampaignException):
    """Исключение при нехватке очков Warchest Points (WP)."""
    def __init__(self, required: int, available: int):
        super().__init__(
            message=f"Недостаточно очков Warchest (WP). Требуется: {required}, доступно: {available}",
            code="INSUFFICIENT_WARCHEST_POINTS"
        )


async def chaos_campaign_exception_handler(request: Request, exc: ChaosCampaignException) -> JSONResponse:
    """Глобальный обработчик кастомных ошибок кампании."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error_code": exc.code,
            "message": exc.message,
            "path": request.url.path
        }
    )