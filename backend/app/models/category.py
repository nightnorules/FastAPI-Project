from sqlalchemy import String
from sqlalchemy.orm import relationship, mapped_column, Mapped
from backend.app.database.base import Base
from backend.app.models.product import Product


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), index=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True)

    products: Mapped[list["Product"]] = relationship(back_populates="category")

    def __repr__(self):
        return f"Id: {self.id}, name: {self.name}"
