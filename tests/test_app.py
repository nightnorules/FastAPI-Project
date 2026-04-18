from httpx import ASGITransport, AsyncClient
import pytest

from backend.app.main import app


@pytest.mark.anyio
async def test_health_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_openapi_contains_core_routes():
    schema = app.openapi()
    paths = schema["paths"]

    assert "/health" in paths
    assert "/api/auth/login" in paths
    assert "/api/products" in paths
