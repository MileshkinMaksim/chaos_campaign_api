import pytest
from httpx import AsyncClient
from app.config import settings
from app.db.models.force import ForceModel


async def test_complete_track_sp_conversion_limit_validation(
    client: AsyncClient, 
    auth_headers: dict, 
    test_force: ForceModel
):
    """Тест срабатывания Pydantic @model_validator при попытке перевести > 200 SP за трек (422 Unprocessable Entity)."""
    track_id = "track-alpha"
    payload = {
        "completed_objectives_ids": ["obj-1"],
        "pilot_performances": [
            {"pilot_id": "pilot-1", "sp_allocated_to_xp": 100},
            {"pilot_id": "pilot-2", "sp_allocated_to_xp": 100},
            {"pilot_id": "pilot-3", "sp_allocated_to_xp": 50}  # Итого: 250 SP > 200 SP limit
        ]
    }

    response = await client.post(
        f"{settings.API_V1_STR}/tracks/{track_id}/complete?force_id={test_force.id}",
        json=payload,
        headers=auth_headers
    )

    assert response.status_code == 422


async def test_complete_track_transactional_success(
    client: AsyncClient, 
    auth_headers: dict, 
    test_force: ForceModel
):
    """Тест успешного подведения итогов трека с зачислением наград, начислением MVP бонуса и обновлением балансов."""
    pilot = test_force.pilots[0]
    track_id = "track-bravo"
    payload = {
        "completed_objectives_ids": ["obj-primary"],
        "pilot_performances": [
            {
                "pilot_id": pilot.id,
                "survived": True,
                "objectives_completed": 1,
                "kills": 2,
                "is_mvp": True,            # +50 bonus XP
                "sp_allocated_to_xp": 80  # 80 SP -> 80 XP
            }
        ],
        "damaged_unit_ids": []
    }

    response = await client.post(
        f"{settings.API_V1_STR}/tracks/{track_id}/complete?force_id={test_force.id}&earned_wp=400&earned_sp=200",
        json=payload,
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    
    assert data["wp_earned"] == 400
    assert data["sp_earned"] == 200
    assert data["total_sp_spent_on_xp"] == 80
    
    # Проверка вычисления XP для MVP: 80 (из SP) + 50 (MVP) = 130 XP
    allocation = data["xp_allocations"][0]
    assert allocation["sp_converted_xp"] == 80
    assert allocation["mvp_bonus_xp"] == 50
    assert allocation["total_xp_gained"] == 130