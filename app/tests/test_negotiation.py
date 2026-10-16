import pytest
from httpx import AsyncClient
from app.config import settings
from app.db.models.force import ForceModel


async def test_negotiate_contract_success(
    client: AsyncClient, 
    auth_headers: dict, 
    test_force: ForceModel
):
    """Тест согласования условий при достаточном рейтинге репутации (10 >= 5)."""
    contract_id = "test-contract-001"
    negotiation_payload = {
        "requested_terms": {
            "base_payment_wp": 600,
            "overhead_sp": 250,
            "command_rights": "Independent",
            "salvage_rights": "Shared",
            "support_rights_percent": 50,
            "transport_coverage_percent": 100
        }
    }

    response = await client.post(
        f"{settings.API_V1_STR}/contracts/{contract_id}/negotiate?force_id={test_force.id}",
        json=negotiation_payload,
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "terms_accepted"


async def test_negotiate_contract_insufficient_reputation(
    client: AsyncClient, 
    auth_headers: dict, 
    test_force: ForceModel,
    test_db
):
    """Тест отклонения условий при низкой репутации отряда."""
    test_force.reputation_score = 2  # Опускаем репутацию ниже требуемой (required=5)
    test_db.add(test_force)
    await test_db.flush()

    contract_id = "test-contract-002"
    negotiation_payload = {
        "requested_terms": {
            "base_payment_wp": 1000,
            "overhead_sp": 500,
            "command_rights": "Independent",
            "salvage_rights": "Full",
            "support_rights_percent": 100,
            "transport_coverage_percent": 100
        }
    }

    response = await client.post(
        f"{settings.API_V1_STR}/contracts/{contract_id}/negotiate?force_id={test_force.id}",
        json=negotiation_payload,
        headers=auth_headers
    )

    assert response.status_code == 400
    data = response.json()
    assert data["error_code"] == "REPUTATION_REQUIREMENT_NOT_MET"