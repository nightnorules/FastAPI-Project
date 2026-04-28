import logging

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.repositories.order import OrderRepository
from backend.app.schemas.order import OrderCreate, OrderResponse, OrderUpdate

logger = logging.getLogger(__name__)


class OrderService:
    def __init__(self, db: AsyncSession):
        self.repository = OrderRepository(db)

    async def create_order(self, user_id: int, order_data: OrderCreate) -> OrderResponse:
        try:
            order = await self.repository.create(user_id, order_data)
            logger.info(f"Order {order.id} created for user {user_id}")
            return OrderResponse.model_validate(order)
        except ValueError as e:
            logger.error(f"Error creating order for user {user_id}: {e}")
            raise

    async def get_user_orders(self, user_id: int) -> list[OrderResponse]:
        orders = await self.repository.get_all_by_user(user_id)
        return [OrderResponse.model_validate(order) for order in orders]

    async def get_order(self, order_id: int, user_id: int) -> OrderResponse | None:
        order = await self.repository.get_by_id(order_id, user_id)
        if order:
            return OrderResponse.model_validate(order)
        return None

    async def update_order_status(
        self, order_id: int, order_data: OrderUpdate, user_id: int
    ) -> OrderResponse | None:
        order = await self.repository.update_status(order_id, order_data, user_id)
        if order:
            logger.info(f"Order {order_id} status updated to {order.status}")
            return OrderResponse.model_validate(order)
        return None

    async def cancel_order(self, order_id: int, user_id: int) -> bool:
        order = await self.repository.get_by_id(order_id, user_id)
        if order and order.status == "pending":
            await self.repository.update_status(order_id, OrderUpdate(status="cancelled"), user_id)
            logger.info(f"Order {order_id} cancelled")
            return True
        return False
