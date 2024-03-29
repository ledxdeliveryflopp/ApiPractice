from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.password.service import PasswordService
from src.settings.depends import get_session
from src.vault.service import VaultService, get_vault_service


async def get_password_service(session: AsyncSession = Depends(get_session),
                               vault_service: VaultService = Depends(get_vault_service)):
    """Инициализация репозитория паролей и сервисов паролей"""
    password_service = PasswordService(session=session, vault_service=vault_service)
    return password_service
