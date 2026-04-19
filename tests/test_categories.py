import pytest
from httpx import AsyncClient
from fastapi import status


@pytest.mark.asyncio
async def test_get_all_categories(client: AsyncClient, test_category):
    response = await client.get("/api/categories")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_category_by_id(client: AsyncClient, test_category):
    response = await client.get(f"/api/categories/{test_category.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == test_category.id
    assert data["name"] == test_category.name


@pytest.mark.asyncio
async def test_get_category_not_found(client: AsyncClient):
    response = await client.get("/api/categories/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_create_category(client: AsyncClient):
    response = await client.post(
        "/api/categories",
        json={"name": "New Category", "description": "New Description"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "New Category"


@pytest.mark.asyncio
async def test_update_category(client: AsyncClient, test_category):
    response = await client.put(
        f"/api/categories/{test_category.id}",
        json={"name": "Updated Category"},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Updated Category"


@pytest.mark.asyncio
async def test_delete_category(client: AsyncClient, test_category):
    response = await client.delete(f"/api/categories/{test_category.id}")
    assert response.status_code == status.HTTP_200_OK
    
    response = await client.get(f"/api/categories/{test_category.id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
