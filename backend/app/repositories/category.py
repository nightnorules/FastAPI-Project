import logging

from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.category import Category
from backend.app.models.product import Product
from backend.app.schemas.category import CategoryCreate, CategoryUpdate

logger = logging.getLogger(__name__)


class CategoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[Category]:
        result = await self.db.execute(select(Category))
        return result.scalars().all()

    async def get_by_id(self, category_id: int) -> Category | None:
        result = await self.db.execute(
            select(Category).where(Category.id == category_id)
        )
        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Category | None:
        result = await self.db.execute(select(Category).where(Category.slug == slug))
        return result.scalar_one_or_none()

    async def count_products(self, category_id: int) -> int:
        result = await self.db.execute(
            select(func.count(Product.id)).where(Product.category_id == category_id)
        )
        return result.scalar_one()

    async def create(self, category_data: CategoryCreate) -> Category:
        db_category = Category(**category_data.model_dump())
        self.db.add(db_category)
        try:
            await self.db.commit()
            await self.db.refresh(db_category)
            return db_category
        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(f"Error creating category: {e}")
            raise

    async def update(
        self, category_id: int, category_data: CategoryUpdate
    ) -> Category | None:
        db_category = await self.get_by_id(category_id)
        if not db_category:
            return None
        for key, value in category_data.model_dump(exclude_unset=True).items():
            setattr(db_category, key, value)
        try:
            await self.db.commit()
            await self.db.refresh(db_category)
            return db_category
        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(f"Error updating category: {e}")
            raise

    async def delete(self, category_id: int) -> bool:
        db_category = await self.get_by_id(category_id)
        if not db_category:
            return False
        await self.db.delete(db_category)
        try:
            await self.db.commit()
            return True
        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(f"Error deleting category: {e}")
            raise
