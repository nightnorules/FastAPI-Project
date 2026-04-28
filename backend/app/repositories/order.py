import logging
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.app.models.order import Order, OrderItem
from backend.app.models.product import Product
from backend.app.schemas.order import OrderCreate, OrderUpdate

logger = logging.getLogger(__name__)


class OrderRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    @staticmethod
    def _order_query():
        return select(Order).options(
            selectinload(Order.items).selectinload(OrderItem.product)
        )
    
    async def get_user_orders(self, user_id: int) -> list[Order]:
        result = await self.db.execute(
            self._order_query().where(Order.user_id == user_id)
        )
        return result.scalars().all()

    async def get_by_id(self, order_id: int, user_id: int | None = None) -> Order | None:
        query = self._order_query().where(Order.id == order_id)
        if user_id:
            query = query.where(Order.user_id == user_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create(self, user_id: int, order_data: OrderCreate) -> Order:
        total_price = Decimal(0)
        items_data = []

        for item_data in order_data.items:
            product_result = await self.db.execute(
                select(Product).where(Product.id == item_data.product_id)
            )
            product = product_result.scalar_one_or_none()
            if not product:
                raise ValueError(f"Product {item_data.product_id} not found")

            item_price = product.price * item_data.quantity
            total_price += item_price
            items_data.append(
                {
                    "product_id": item_data.product_id,
                    "quantity": item_data.quantity,
                    "price": product.price,
                }
            )

        db_order = Order(user_id=user_id, total_price=total_price)
        
        for item_data in items_data:
            order_item = OrderItem(**item_data)
            db_order.items.append(order_item)

        self.db.add(db_order)
        await self.db.flush()
        await self.db.refresh(db_order)
        return db_order

    async def update_status(self, order_id: int, order_data: OrderUpdate, user_id: int | None = None) -> Order | None:
        db_order = await self.get_by_id(order_id, user_id)
        if not db_order:
            return None

        if order_data.status:
            db_order.status = order_data.status

        self.db.add(db_order)
        await self.db.flush()
        await self.db.refresh(db_order)
        return db_order

    async def delete(self, order_id: int, user_id: int | None = None) -> bool:
        db_order = await self.get_by_id(order_id, user_id)
        if not db_order:
            return False

        await self.db.delete(db_order)
        await self.db.flush()
        return True
