from pydantic import BaseModel, ConfigDict, Field


class CategoryBase(BaseModel):
    name: str = Field(min_length=5, max_length=100, description="Category name")
    slug: str = Field(
        min_length=5, max_length=100, description="URL-friendly category name"
    )


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: str | None = Field(
        None, min_length=5, max_length=100, description="Category name"
    )
    slug: str | None = Field(
        None, min_length=5, max_length=100, description="URL-friendly category name"
    )


class CategoryResponse(CategoryBase):
    id: int = Field(description="Unique category identifier")

    model_config = ConfigDict(from_attributes=True)
