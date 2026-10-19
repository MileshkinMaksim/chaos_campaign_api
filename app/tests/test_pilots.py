import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import settings
from app.db.models.force import ForceModel


async def test_upgrade_pilot_gunnery_success(
    client: AsyncClient, 
    auth_headers: dict, 
    test_force: ForceModel,
    test_db: AsyncSession
):
    """Тест успешного улучшения Gunnery с 4 до 3 за 300 XP."""
    pilot = test_force.pilots[0]
    pilot.experience_points = 500  # Добавляем достаточное количество XP (требуется 300 XP)
    test_db.add(pilot)
    await test_db.flush()

    initial_xp = pilot.experience_points

    response = await client.post(
        f"{settings.API_V1_STR}/pilots/{pilot.id}/upgrade",
        json={"upgrade_type": "gunnery"},
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["gunnery"] == 3
    assert data["experience_points"] == initial_xp - 300


async def test_upgrade_pilot_insufficient_xp(
    client: AsyncClient, 
    auth_headers: dict, 
    test_force: ForceModel,
    test_db: AsyncSession
):
    """Тест ошибки 400 Bad Request при нехватке XP у пилота."""
    pilot = test_force.pilots[0]
    pilot.experience_points = 50  # Устанавливаем заведомо малое значение
    test_db.add(pilot)
    await test_db.flush()

    response = await client.post(
        f"{settings.API_V1_STR}/pilots/{pilot.id}/upgrade",
        json={"upgrade_type": "gunnery"},
        headers=auth_headers
    )

    assert response.status_code == 400
    data = response.json()
    assert data["error_code"] == "INSUFFICIENT_XP"