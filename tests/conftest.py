import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.core.config.config import TEST_ASYNC_DATABASE_URL
from main import app
from app.database.database import Base, get_async_session


@pytest_asyncio.fixture(scope="function")
async def test_engine():
    """Создаём движок внутри фикстуры (в правильном event loop) и корректно очищаем."""
    engine = create_async_engine(TEST_ASYNC_DATABASE_URL, echo=False)
    try:
        yield engine
    finally:
        await engine.dispose()


@pytest_asyncio.fixture(scope="function")
def TestSessionLocal(test_engine):
    """Создаём sessionmaker в том же цикле (не async)."""
    return async_sessionmaker(
        bind=test_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )


@pytest_asyncio.fixture(scope="function")
async def db_session(test_engine, TestSessionLocal):
    """Создаёт таблицы перед тестом и удаляет после"""
    # Создаём все таблицы
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Возвращаем сессию для теста
    async with TestSessionLocal() as session:
        yield session

    # Удаляем все таблицы после теста
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client(db_session, TestSessionLocal):
    """HTTP-клиент с подменой БД"""
    async def override_get_async_session():
        async with TestSessionLocal() as session:
            yield session

    app.dependency_overrides[get_async_session] = override_get_async_session
    try:
        async with AsyncClient(
                base_url="http://test",
                transport=ASGITransport(app=app),
                timeout=10.0,
        ) as ac:
            yield ac
    finally:
        # Всегда очищаем переопределения
        app.dependency_overrides.clear()
