from fastapi import Depends
from starlette.requests import Request
from src.authorization.repository import TokenRepository
from src.authorization.service import TokenService
from src.settings.depends import get_project_service
from src.settings.service import SessionService


async def get_token_service(request: Request, session_service:
                            SessionService = Depends(get_project_service)):
    """Инициализация репозитория токенов и сервисов токенов"""
    token_repository = TokenRepository(session_service=session_service, request=request)
    token_service = TokenService(repository=token_repository)
    return token_service
