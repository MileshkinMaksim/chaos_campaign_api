from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.models.force import ForceModel
from app.db.models.user import UserModel
from app.dependencies.auth import get_current_user


async def verify_force_ownership(
    force_id: str,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> ForceModel:
    """Проверяет существование отряда в СУБД и права доступа текущего пользователя."""
    stmt = (
        select(ForceModel)
        .where(ForceModel.id == force_id)
        .options(
            selectinload(ForceModel.units),
            selectinload(ForceModel.pilots)
        )
    )
    result = await db.execute(stmt)
    force = result.scalar_one_or_none()

    if force is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Отряд с ID '{force_id}' не найден"
        )

    if force.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="У вас нет прав для управления этим отрядом"
        )

    return force