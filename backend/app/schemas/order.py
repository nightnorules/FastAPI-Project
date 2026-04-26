from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from backend.app.models.order import OrderStatus


class OrderItemBase(BaseModel):
    product_id: int = Field(..., description="Product ID")
    quantity: int = Field(..., ge=1, description="Quantity")


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemResponse(OrderItemBase):
    id: int
    price: Decimal
    
    model_config = ConfigDict(from_attributes=True)


class OrderBase(BaseModel):
    pass


class OrderCreate(OrderBase):
    items: list[OrderItemCreate] = Field(..., min_items=1, description="Order items")


class OrderUpdate(BaseModel):
    status: OrderStatus | None = None


class OrderResponse(OrderBase):
    id: int = Field(description="Order ID")
    user_id: int = Field(description="User ID")
    status: OrderStatus = Field(description="Order status")
    total_price: Decimal = Field(description="Total order price")
    created_at: datetime
    updated_at: datetime
    items: list[OrderItemResponse]

    model_config = ConfigDict(from_attributes=True)


class OrderListResponse(BaseModel):
    orders: list[OrderResponse]
