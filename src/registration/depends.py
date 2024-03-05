from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.registration.repository import UserRepository
from src.registration.schemas import UserCreateSchemas
from src.registration.service import UserService
from src.settings.depends import get_session


async def get_user_service(user_schemas: UserCreateSchemas,
                           session: AsyncSession = Depends(get_session)):
    """Инициализация репозитория пользователей и сервисов пользователей"""
    user_repository = UserRepository(session=session, user_schemas=user_schemas)
    user_service = UserService(repository=user_repository)
    return user_service
