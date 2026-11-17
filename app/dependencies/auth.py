from typing import Optional
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyCookie, OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.config import settings
from app.db.database import get_db
from app.db.models.force import ForceModel
from app.db.models.user import UserModel
from app.schemas.auth import TokenData

cookie_scheme = APIKeyCookie(
    name=settings.COOKIE_NAME,
    auto_error=False,
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/token",
    auto_error=False,
)


async def get_current_user(
    cookie_token: Optional[str] = Depends(cookie_scheme),
    header_token: Optional[str] = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> UserModel:
    """Извлекает и валидирует текущего пользователя из HttpOnly Cookie (или Bearer-заголовка)."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось валидировать учетные данные",
    )

    token = cookie_token or header_token
    if not token:
        raise credentials_exception

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        commander_id: Optional[str] = payload.get("sub") or payload.get("commander_id")
        if commander_id is None:
            raise credentials_exception
        token_data = TokenData(commander_id=commander_id)
    except jwt.PyJWTError:
        raise credentials_exception

    stmt = select(UserModel).where(UserModel.id == token_data.commander_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь неактивен",
        )

    return user


async def verify_force_ownership(
    force_id: str,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ForceModel:
    stmt = (
        select(ForceModel)
        .where(ForceModel.id == force_id, ForceModel.owner_id == current_user.id)
        .options(selectinload(ForceModel.units), selectinload(ForceModel.pilots))
    )
    result = await db.execute(stmt)
    force = result.scalar_one_or_none()
    if not force:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Отряд не найден или доступ запрещен",
        )
    return force