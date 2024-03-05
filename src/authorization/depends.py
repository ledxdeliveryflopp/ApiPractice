from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.authorization.repository import TokenRepository
from src.authorization.schemas import LoginSchemas
from src.authorization.service import TokenService
from src.settings.depends import get_session


async def get_token_service(login_schemas: LoginSchemas, session: AsyncSession = Depends(
                            get_session)):
    """Инициализация репозитория токенов и сервисов токенов"""
    token_repository = TokenRepository(session=session, login_schemas=login_schemas)
    token_service = TokenService(repository=token_repository)
    return token_service
