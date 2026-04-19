import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from backend.app.main import app
from backend.app.database.session import get_db
from backend.app.database.base import Base
from backend.app.models import User, Category, Product
from backend.app.services.auth import AuthService
import os

DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture
async def engine():
    engine = create_async_engine(
        DATABASE_URL,
        echo=False,
        connect_args={"check_same_thread": False},
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
async def async_session_local(engine):
    async_session = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    yield async_session


@pytest.fixture
async def db_session(async_session_local):
    async with async_session_local() as session:
        yield session


@pytest.fixture
def override_get_db(async_session_local):
    async def _get_db():
        async with async_session_local() as session:
            yield session

    return _get_db


@pytest.fixture
async def client(override_get_db):
    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.fixture
async def test_user(db_session):
    from backend.app.schemas.user import UserCreate

    auth_service = AuthService(db_session)
    user_data = UserCreate(
        email="test@example.com", password="Test@1234", username="testuser"
    )
    user = await auth_service.register_user(user_data)
    return user


@pytest.fixture
async def auth_token(db_session, test_user):
    auth_service = AuthService(db_session)
    token = auth_service.create_access_token(test_user.id, test_user.email)
    return token


@pytest.fixture
async def test_category(db_session):
    from backend.app.repositories.category import CategoryRepository

    repo = CategoryRepository(db_session)
    from backend.app.schemas.category import CategoryCreate

    category = await repo.create(CategoryCreate(name="Test Category"))
    return category


@pytest.fixture
async def test_product(db_session, test_category):
    from backend.app.repositories.products import ProductRepository
    from backend.app.schemas.product import ProductCreate

    repo = ProductRepository(db_session)
    product = await repo.create(
        ProductCreate(
            name="Test Product",
            description="Test Description",
            price=99.99,
            category_id=test_category.id,
        )
    )
    return product
