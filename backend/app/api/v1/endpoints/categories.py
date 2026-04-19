from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.database.session import get_db
from backend.app.schemas.category import (CategoryCreate, CategoryResponse,
                                          CategoryUpdate)
from backend.app.services.category import CategoryService

router = APIRouter(prefix="/api/categories", tags=["categories"])


@router.get("", response_model=list[CategoryResponse], summary="Get all categories")
async def list_categories(db: AsyncSession = Depends(get_db)):
    service = CategoryService(db)
    return await service.get_all_categories()


@router.get(
    "/{category_id}", response_model=CategoryResponse, summary="Get category by ID"
)
async def get_category(category_id: int, db: AsyncSession = Depends(get_db)):
    service = CategoryService(db)
    return await service.get_category_by_id(category_id)


@router.get(
    "/slug/{slug}", response_model=CategoryResponse, summary="Get category by slug"
)
async def get_category_by_slug(slug: str, db: AsyncSession = Depends(get_db)):
    service = CategoryService(db)
    return await service.get_category_by_slug(slug)


@router.post(
    "",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create category",
)
async def create_category(category: CategoryCreate, db: AsyncSession = Depends(get_db)):
    service = CategoryService(db)
    return await service.create_category(category)


@router.put(
    "/{category_id}", response_model=CategoryResponse, summary="Update category"
)
async def update_category(
    category_id: int, category: CategoryUpdate, db: AsyncSession = Depends(get_db)
):
    service = CategoryService(db)
    return await service.update_category(category_id, category)


@router.delete("/{category_id}", summary="Delete category")
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db)):
    service = CategoryService(db)
    return await service.delete_category(category_id)
