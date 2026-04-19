from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Numeric

from backend.app.database.base import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), index=True)
    description: Mapped[str | None]
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), index=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), index=True)
    image_url: Mapped[str | None] = mapped_column(String(500))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    category: Mapped["Category"] = relationship(back_populates="products")

    def __repr__(self):
        return f"Product(id={self.id}, name={self.name}, price={self.price})"
