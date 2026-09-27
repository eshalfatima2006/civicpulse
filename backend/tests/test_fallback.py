import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.providers.triage.simulated import SimulatedTriage
from app.routes import complaints


@pytest.mark.asyncio
async def test_failing_provider_uses_rules_fallback(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(complaints.triage_service, "provider", SimulatedTriage.failing())

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/complaints",
            json={"text": "There is an urgent water leak", "location": "Main Street"},
        )

    assert response.status_code == 201
    assert response.json()["triaged_by"] == "rules:fallback"
