import pytest
from httpx import AsyncClient
from fastapi import status


@pytest.mark.asyncio
async def test_get_all_products(client: AsyncClient, test_product):
    response = await client.get("/api/products")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.asyncio
async def test_get_product_by_id(client: AsyncClient, test_product):
    response = await client.get(f"/api/products/{test_product.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == test_product.id
    assert data["name"] == test_product.name


@pytest.mark.asyncio
async def test_get_product_not_found(client: AsyncClient):
    response = await client.get("/api/products/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_get_products_by_category(client: AsyncClient, test_product, test_category):
    response = await client.get(f"/api/products/category/{test_category.id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.asyncio
async def test_search_products(client: AsyncClient, test_product):
    response = await client.get(
        "/api/products/search", params={"search": "Test"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_create_product(client: AsyncClient, test_category):
    response = await client.post(
        "/api/products",
        json={
            "name": "New Product",
            "description": "New Description",
            "price": 49.99,
            "category_id": test_category.id,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "New Product"
    assert data["price"] == 49.99


@pytest.mark.asyncio
async def test_create_product_invalid_category(client: AsyncClient):
    response = await client.post(
        "/api/products",
        json={
            "name": "New Product",
            "description": "New Description",
            "price": 49.99,
            "category_id": 99999,
        },
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_update_product(client: AsyncClient, test_product):
    response = await client.put(
        f"/api/products/{test_product.id}",
        json={
            "name": "Updated Product",
            "price": 79.99,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Updated Product"
    assert data["price"] == 79.99


@pytest.mark.asyncio
async def test_update_product_not_found(client: AsyncClient):
    response = await client.put(
        "/api/products/99999",
        json={"name": "Updated"},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_product(client: AsyncClient, test_product):
    response = await client.delete(f"/api/products/{test_product.id}")
    assert response.status_code == status.HTTP_200_OK
    
    response = await client.get(f"/api/products/{test_product.id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_product_not_found(client: AsyncClient):
    response = await client.delete("/api/products/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
