from datetime import datetime
from decimal import Decimal

from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field, computed_field

from backend.app.schemas.category import CategoryResponse


class ProductBase(BaseModel):
    name: str = Field(..., min_length=5, max_length=100, description="Product name")
    description: str | None = Field(None, description="Product description")
    price: Decimal = Field(..., gt=0, decimal_places=2, description="Product price")
    category_id: int = Field(..., description="Category ID")
    image_url: AnyHttpUrl | None = Field(None, description="Product image URL")


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: Decimal | None = None
    category_id: int | None = None
    image_url: AnyHttpUrl | None = None


class ProductResponse(ProductBase):
    id: int = Field(description="Unique product identifier")
    created_at: datetime
    category: CategoryResponse = Field(description="Product category")

    model_config = ConfigDict(from_attributes=True)


class ProductListResponse(BaseModel):
    products: list[ProductResponse]

    @computed_field
    @property
    def total(self) -> int:
        return len(self.products)
