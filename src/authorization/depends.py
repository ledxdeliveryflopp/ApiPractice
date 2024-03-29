from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from src.authorization.repository import TokenRepository
from src.authorization.service import TokenService
from src.settings.depends import get_session_service, get_session
from src.settings.service import SessionService


async def get_token_service(request: Request, session_service:
                            SessionService = Depends(get_session_service),
                            session: AsyncSession = Depends(get_session)):
    """Инициализация репозитория токенов и сервисов токенов"""
    token_repository = TokenRepository(request=request, session=session)
    token_service = TokenService(repository=token_repository, session_service=session_service)
    return token_service
