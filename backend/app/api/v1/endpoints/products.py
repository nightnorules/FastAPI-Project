from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.database.session import get_db
from backend.app.schemas.product import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
)
from backend.app.services.product import ProductService

router = APIRouter(prefix="/api/products", tags=["products"])


@router.get("", response_model=list[ProductResponse], summary="Get all products")
async def list_products(db: AsyncSession = Depends(get_db)):
    service = ProductService(db)
    return await service.get_all_products()


@router.get("/search", response_model=list[ProductResponse], summary="Search products")
async def search_products(
    search: str | None = None,
    category_id: int | None = None,
    min_price: float | None = Query(None, ge=0),
    max_price: float | None = Query(None, ge=0),
    db: AsyncSession = Depends(get_db),
):
    service = ProductService(db)
    return await service.search_products(search, category_id, min_price, max_price)


@router.get(
    "/{product_id}", response_model=ProductResponse, summary="Get product by ID"
)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    service = ProductService(db)
    return await service.get_product_by_id(product_id)


@router.get(
    "/category/{category_id}",
    response_model=list[ProductResponse],
    summary="Get products by category",
)
async def get_products_by_category(
    category_id: int, db: AsyncSession = Depends(get_db)
):
    service = ProductService(db)
    return await service.get_products_by_category(category_id)


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create product",
)
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    service = ProductService(db)
    return await service.create_product(product)


@router.put("/{product_id}", response_model=ProductResponse, summary="Update product")
async def update_product(
    product_id: int, product: ProductUpdate, db: AsyncSession = Depends(get_db)
):
    service = ProductService(db)
    return await service.update_product(product_id, product)


@router.delete("/{product_id}", summary="Delete product")
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    service = ProductService(db)
    return await service.delete_product(product_id)
