import logging
from typing import List

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.repositories.category import CategoryRepository
from backend.app.schemas.category import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
)

logger = logging.getLogger(__name__)


class CategoryService:
    def __init__(self, db: AsyncSession):
        self.repository = CategoryRepository(db)

    async def get_all_categories(self) -> List[CategoryResponse]:
        categories = await self.repository.get_all()
        return [CategoryResponse.model_validate(category) for category in categories]

    async def get_category_by_id(self, category_id: int) -> CategoryResponse:
        category = await self.repository.get_by_id(category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {category_id} not found",
            )
        return CategoryResponse.model_validate(category)

    async def get_category_by_slug(self, slug: str) -> CategoryResponse:
        category = await self.repository.get_by_slug(slug)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with slug '{slug}' not found",
            )
        return CategoryResponse.model_validate(category)

    async def create_category(self, category_data: CategoryCreate) -> CategoryResponse:
        try:
            category = await self.repository.create(category_data)
            return CategoryResponse.model_validate(category)
        except IntegrityError:
            logger.warning(f"Duplicate slug attempted: {category_data.slug}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Category with slug '{category_data.slug}' already exists",
            )

    async def update_category(
        self, category_id: int, category_data: CategoryUpdate
    ) -> CategoryResponse:
        try:
            category = await self.repository.update(category_id, category_data)
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Category with id {category_id} not found",
                )
            return CategoryResponse.model_validate(category)
        except IntegrityError:
            logger.warning(f"Duplicate slug in update: {category_data.slug}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Category with slug '{category_data.slug}' already exists",
            )

    async def delete_category(self, category_id: int) -> dict:
        product_count = await self.repository.count_products(category_id)
        if product_count > 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Category with id {category_id} cannot be deleted because it contains products",
            )

        success = await self.repository.delete(category_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {category_id} not found",
            )
        return {"message": f"Category {category_id} deleted successfully"}
