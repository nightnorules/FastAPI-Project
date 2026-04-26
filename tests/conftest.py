import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from backend.app.database.base import Base
from backend.app.database.session import get_db
from backend.app.main import app
from backend.app.models import Category, Product, User
from backend.app.services.auth import AuthService

DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture
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


@pytest_asyncio.fixture
async def async_session_local(engine):
    async_session = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    yield async_session


@pytest_asyncio.fixture
async def db_session(async_session_local):
    async with async_session_local() as session:
        yield session


@pytest_asyncio.fixture
async def client(db_session):
    async def get_db_override():
        yield db_session

    app.dependency_overrides[get_db] = get_db_override
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def test_user(db_session):
    from backend.app.schemas.user import UserCreate

    auth_service = AuthService(db_session)
    user_data = UserCreate(
        email="test@example.com", password="Test1234", username="testuser"
    )
    user = await auth_service.register_user(user_data)
    return user


@pytest_asyncio.fixture
async def auth_token(db_session, test_user):
    auth_service = AuthService(db_session)
    token = auth_service.create_access_token(test_user.id, test_user.email)
    return token


@pytest_asyncio.fixture
async def test_category(db_session):
    from backend.app.repositories.category import CategoryRepository
    from backend.app.schemas.category import CategoryCreate

    repo = CategoryRepository(db_session)
    category = await repo.create(
        CategoryCreate(name="Test Category", slug="test-category")
    )
    return category


@pytest_asyncio.fixture
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
