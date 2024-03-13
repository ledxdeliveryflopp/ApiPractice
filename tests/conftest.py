import asyncio
from unittest.mock import Mock

import pytest
import pytest_asyncio
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.registration.models import UserModel
from src.registration.repository import UserRepository
from src.registration.schemas import UserCreateSchemas
from src.registration.service import UserService
from src.registration.utils import hash_password
from src.settings.db import Base
from src.settings.settings import settings
from src.vault.service import client


@pytest.fixture(scope="session", autouse=True)
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


engine = create_async_engine(
    url=f"postgresql+asyncpg://{settings.sql_settings.sql_user}:"
        f"{settings.sql_settings.sql_password}@{settings.sql_settings.sql_host}:"
        f"{settings.sql_settings.sql_port}/{settings.sql_settings.sql_name}",
    echo=False)

database_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

session = AsyncSession(engine)


# async def override_get_session() -> AsyncSession:
#     async with database_session() as session:
#         yield session


def session_mock():
    return Mock(name="db_session_mock", spec_set=AsyncSession)


@pytest.fixture
async def get_user_service_override(user_schemas: UserCreateSchemas,
                                    session: AsyncSession = Depends(session_mock)):
    """Инициализация репозитория пользователей и сервисов пользователей"""
    user_repository = UserRepository(session=session, user_schemas=user_schemas)
    user_service = UserService(repository=user_repository)
    return user_service


# @pytest.fixture()
# async def prepare_database():
#     """Создание таблиц и запись данных в тестувую БД"""
#     user = UserModel(username="test", email="test@test.ru")
#     session.add(user)
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#     await session.commit()
#     yield
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)


# @pytest.fixture()
# async def create_delete_secret_vault():
#     """Сохранение тестового пароля в Vault"""
#     password = hash_password(password="testprofilepassword")
#     client.secrets.kv.v2.create_or_update_secret(
#         mount_point=settings.vault_settings.vault_mount,
#         path='test@test.ru-secret-password',
#         secret=dict(password=password),
#     )


@pytest.fixture(scope="session")
def app_session():
    from main import authorization
    return authorization


@pytest_asyncio.fixture
async def AppSetUp(app_session):
    from src.settings.depends import get_session
    from src.registration.depends import get_user_service

    app_session.dependency_overrides[get_session] = session_mock
    app_session.dependency_overrides[get_user_service] = get_user_service_override

    return app_session
