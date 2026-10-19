from fastapi import Request, status
from fastapi.responses import JSONResponse


class ChaosCampaignException(Exception):
    """Базовое исключение бизнес-логики Chaos Campaign."""
    def __init__(self, message: str, code: str):
        self.message = message
        self.code = code


class InsufficientSupportPointsError(Exception):
    """Исключение при нехватке Support Points (SP)."""
    def __init__(self, required: int, available: int):
        self.required = required
        self.available = available
        self.message = f"Недостаточно SP: требуется {required}, доступно {available}"
        super().__init__(self.message)

class InvalidStartingForceConfigError(Exception):
    """Исключение при нарушении правил создания стартового отряда."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class InsufficientXPError(Exception):
    """Исключение при нехватке XP у пилота."""
    def __init__(self, required: int, available: int):
        self.required = required
        self.available = available
        self.message = f"Недостаточно XP: требуется {required}, доступно {available}"
        super().__init__(self.message)

class ReputationRequirementNotMetError(Exception):
    """Исключение при недостаточной репутации для контракта."""
    def __init__(self, required: int, current: int):
        self.required = required
        self.current = current
        self.message = f"Недостаточный уровень репутации: требуется {required}, текущая {current}"
        super().__init__(self.message)


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