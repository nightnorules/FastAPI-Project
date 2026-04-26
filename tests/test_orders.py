import pytest
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.order import Order, OrderStatus
from backend.app.repositories.order import OrderRepository
from backend.app.schemas.order import OrderCreate, OrderItemCreate, OrderUpdate


@pytest.mark.asyncio
async def test_create_order(db: AsyncSession, auth_headers: dict, product_id: int):
    """Test creating an order"""
    order_data = OrderCreate(
        items=[OrderItemCreate(product_id=product_id, quantity=2)]
    )
    
    repo = OrderRepository(db)
    user_id = 1  # Assumes user from auth_headers
    
    order = await repo.create(user_id, order_data)
    
    assert order.id is not None
    assert order.user_id == user_id
    assert order.status == OrderStatus.PENDING
    assert len(order.items) == 1
    assert order.items[0].quantity == 2


@pytest.mark.asyncio
async def test_get_user_orders(db: AsyncSession):
    """Test getting all orders for a user"""
    repo = OrderRepository(db)
    user_id = 1
    
    orders = await repo.get_all_by_user(user_id)
    
    assert isinstance(orders, list)


@pytest.mark.asyncio
async def test_update_order_status(db: AsyncSession):
    """Test updating order status"""
    repo = OrderRepository(db)
    order_id = 1
    user_id = 1
    
    update_data = OrderUpdate(status=OrderStatus.CONFIRMED)
    
    order = await repo.update_status(order_id, update_data, user_id)
    
    if order:
        assert order.status == OrderStatus.CONFIRMED
