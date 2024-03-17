from fastapi import Depends
from src.registration.repository import UserRepository
from src.registration.schemas import UserCreateSchemas
from src.registration.service import UserService
from src.settings.service import SessionService
from src.settings.depends import get_project_service


async def get_user_service(user_schemas: UserCreateSchemas,
                           session_service: SessionService = Depends(get_project_service)):
    """Инициализация репозитория пользователей и сервисов пользователей"""
    user_repository = UserRepository(user_schemas=user_schemas, session_service=session_service)
    user_service = UserService(repository=user_repository)
    return user_service
