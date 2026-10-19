import pytest
from httpx import AsyncClient
from app.config import settings
from app.db.models.force import ForceModel


async def test_complete_track_transactional_success(client: AsyncClient, auth_headers: dict, test_force: ForceModel):
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
                "is_mvp": True,
                "sp_allocated_to_xp": 80
            }
        ],
        "damaged_unit_ids": []
    }

    response = await client.post(
        f"{settings.API_V1_STR}/tracks/{track_id}/complete?force_id={test_force.id}&earned_sp=400",
        json=payload,
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    
    assert data["sp_earned"] == 400
    assert data["total_sp_spent_on_xp"] == 80
    assert data["net_sp_gained"] == 320