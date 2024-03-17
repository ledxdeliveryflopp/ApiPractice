from fastapi import Depends
from src.authorization.repository import TokenRepository
from src.authorization.schemas import LoginSchemas
from src.authorization.service import TokenService
from src.settings.depends import get_project_service
from src.settings.service import SessionService


async def get_token_service(login_schemas: LoginSchemas,
                            session_service: SessionService = Depends(get_project_service)):
    """Инициализация репозитория токенов и сервисов токенов"""
    token_repository = TokenRepository(login_schemas=login_schemas, session_service=session_service)
    token_service = TokenService(repository=token_repository)
    return token_service
