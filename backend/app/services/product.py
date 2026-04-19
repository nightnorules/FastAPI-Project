import logging
from typing import List

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.cache import get_cache
from backend.app.repositories.category import CategoryRepository
from backend.app.repositories.products import ProductRepository
from backend.app.schemas.product import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
)

logger = logging.getLogger(__name__)


class ProductService:
    def __init__(self, db: AsyncSession):
        self.repository = ProductRepository(db)
        self.category_repository = CategoryRepository(db)
        self.cache = get_cache()

    async def get_product_by_id(self, product_id: int) -> ProductResponse:
        cache_key = f"product:{product_id}"
        cached = self.cache.get(cache_key)
        if cached:
            logger.info(f"Cache hit for product {product_id}")
            return ProductResponse(**cached)

        product = await self.repository.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {product_id} not found",
            )

        response = ProductResponse.model_validate(product)
        self.cache.set(cache_key, response.model_dump(), ttl=600)
        return response

    async def get_all_products(self) -> List[ProductResponse]:
        products = await self.repository.get_all()
        return [ProductResponse.model_validate(product) for product in products]

    async def get_products_by_category(self, category_id: int) -> List[ProductResponse]:
        category = await self.category_repository.get_by_id(category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {category_id} not found",
            )

        products = await self.repository.get_by_category(category_id)
        return [ProductResponse.model_validate(product) for product in products]

    async def create_product(self, product_data: ProductCreate) -> ProductResponse:
        category = await self.category_repository.get_by_id(product_data.category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {product_data.category_id} not found",
            )

        try:
            product = await self.repository.create(product_data)
            response = ProductResponse.model_validate(product)
            self.cache.delete(f"category:{product_data.category_id}")
            return response
        except IntegrityError as e:
            logger.error(f"Error creating product: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid product data"
            )

    async def update_product(
        self, product_id: int, product_data: ProductUpdate
    ) -> ProductResponse:
        if product_data.category_id:
            category = await self.category_repository.get_by_id(
                product_data.category_id
            )
            if not category:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Category with id {product_data.category_id} not found",
                )

        try:
            product = await self.repository.update(product_id, product_data)
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product with id {product_id} not found",
                )
            response = ProductResponse.model_validate(product)
            self.cache.delete(f"product:{product_id}")
            return response
        except IntegrityError as e:
            logger.error(f"Error updating product: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid product data"
            )

    async def delete_product(self, product_id: int) -> dict:
        success = await self.repository.delete(product_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {product_id} not found",
            )
        self.cache.delete(f"product:{product_id}")
        return {"message": f"Product {product_id} deleted successfully"}

    async def search_products(
        self,
        search: str | None = None,
        category_id: int | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
    ) -> List[ProductResponse]:
        products = await self.repository.get_filtered(
            search, category_id, min_price, max_price
        )
        return [ProductResponse.model_validate(product) for product in products]
