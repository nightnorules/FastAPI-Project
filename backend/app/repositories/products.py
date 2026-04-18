from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload
from backend.app.models.product import Product
from backend.app.schemas.product import ProductCreate, ProductUpdate
import logging

logger = logging.getLogger(__name__)


class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    @staticmethod
    def _product_query():
        return select(Product).options(selectinload(Product.category))

    async def get_all(self) -> list[Product]:
        result = await self.db.execute(self._product_query())
        return result.scalars().all()

    async def get_filtered(
        self,
        search: str | None = None,
        category_id: int | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
    ) -> list[Product]:
        query = self._product_query()

        if search:
            query = query.where(Product.name.ilike(f"%{search}%"))
        if category_id:
            query = query.where(Product.category_id == category_id)
        if min_price is not None:
            query = query.where(Product.price >= min_price)
        if max_price is not None:
            query = query.where(Product.price <= max_price)

        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_id(self, product_id: int) -> Product | None:
        result = await self.db.execute(
            self._product_query().where(Product.id == product_id)
        )
        return result.scalar_one_or_none()

    async def get_by_category(self, category_id: int) -> list[Product]:
        result = await self.db.execute(
            self._product_query().where(Product.category_id == category_id)
        )
        return result.scalars().all()

    async def create(self, product_data: ProductCreate) -> Product:
        db_product = Product(**product_data.model_dump())
        self.db.add(db_product)
        try:
            await self.db.commit()
            return await self.get_by_id(db_product.id)
        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(f"Error creating product: {e}")
            raise

    async def update(self, product_id: int, product_data: ProductUpdate) -> Product | None:
        db_product = await self.get_by_id(product_id)
        if not db_product:
            return None
        for key, value in product_data.model_dump(exclude_unset=True).items():
            setattr(db_product, key, value)
        try:
            await self.db.commit()
            return await self.get_by_id(product_id)
        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(f"Error updating product: {e}")
            raise

    async def delete(self, product_id: int) -> bool:
        db_product = await self.get_by_id(product_id)
        if not db_product:
            return False
        await self.db.delete(db_product)
        try:
            await self.db.commit()
            return True
        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(f"Error deleting product: {e}")
            raise
