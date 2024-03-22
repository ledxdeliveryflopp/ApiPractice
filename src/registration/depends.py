from fastapi import Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from src.registration.repository import UserRepository
from src.registration.schemas import UserCreateSchemas
from src.registration.service import UserService
from src.settings.service import SessionService
from src.settings.depends import get_project_service, get_session


async def get_user_service(user_schemas: UserCreateSchemas, background_tasks: BackgroundTasks,
                           session_service: SessionService = Depends(get_project_service),
                           session: AsyncSession = Depends(get_session)):
    """Инициализация репозитория пользователей и сервисов пользователей"""
    user_repository = UserRepository(user_schemas=user_schemas, session_service=session_service,
                                     session=session)
    user_service = UserService(repository=user_repository, background_tasks=background_tasks)
    return user_service
