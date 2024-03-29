from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.password.repository import PasswordRepository
from src.password.service import PasswordService
from src.settings.depends import get_session, get_session_service
from src.settings.service import SessionService


async def get_password_service(session: AsyncSession = Depends(get_session),
                               session_service: SessionService = Depends(get_session_service)):
    """Инициализация репозитория паролей и сервисов паролей"""
    password_repository = PasswordRepository(session=session)
    password_service = PasswordService(password_repository=password_repository,
                                       session_service=session_service)
    return password_service
