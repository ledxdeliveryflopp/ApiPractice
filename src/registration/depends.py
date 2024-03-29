from fastapi import Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from src.registration.repository import UserRepository
from src.registration.schemas import UserCreateSchemas
from src.registration.service import UserService
from src.settings.depends import get_session


async def get_user_service(user_schemas: UserCreateSchemas, background_tasks: BackgroundTasks,
                           session: AsyncSession = Depends(get_session)):
    """Инициализация репозитория пользователей и сервисов пользователей"""
    user_repository = UserRepository(user_schemas=user_schemas, session=session)
    user_service = UserService(background_tasks=background_tasks, repository=user_repository)
    return user_service
