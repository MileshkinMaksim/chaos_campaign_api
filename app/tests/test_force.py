import pytest
from httpx import AsyncClient
from app.config import settings


async def test_create_force_v6_success(client: AsyncClient, auth_headers: dict):
    payload = {
        "name": "Iron Hand Mercenaries",
        "sponsoring_faction": "Draconis Combine",
        "starting_pilot_names": ["Kenshin", "Saito"],
        "selected_mechs": [
            {"chassis": "Panther", "model": "PNT-9R", "tonnage": 35, "weight_class": "Light", "bv2": 769},
            {"chassis": "Dragon", "model": "DRG-1N", "tonnage": 60, "weight_class": "Heavy", "bv2": 1125}
        ]
    }

    response = await client.post(f"{settings.API_V1_STR}/forces/", json=payload, headers=auth_headers)

    assert response.status_code == 201
    data = response.json()
    assert data["support_points"] == 3000
    assert data["reputation_score"] == 1
    assert len(data["pilots"]) == 2
    assert data["pilots"][0]["experience_points"] == 150
    assert len(data["units"]) == 2


async def test_create_force_v6_exceed_bv2_limit(client: AsyncClient, auth_headers: dict):
    payload = {
        "name": "Heavy Assault Mercs",
        "sponsoring_faction": "Draconis Combine",
        "starting_pilot_names": ["Pilot A", "Pilot B"],
        "selected_mechs": [
            {"chassis": "Atlas", "model": "AS7-D", "tonnage": 100, "weight_class": "Assault", "bv2": 1897},
            {"chassis": "Awesome", "model": "AWS-8Q", "tonnage": 80, "weight_class": "Assault", "bv2": 1605}
        ]  # Итого: 3502 BV2 > 3000 BV2
    }

    response = await client.post(f"{settings.API_V1_STR}/forces/", json=payload, headers=auth_headers)

    assert response.status_code == 422