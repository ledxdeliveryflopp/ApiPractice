from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.authorization.service import TokenService
from src.settings.depends import get_session
from src.vault.service import VaultService, get_vault_service


async def get_token_service(session: AsyncSession = Depends(get_session),
                            vault_service: VaultService = Depends(get_vault_service)):
    """Инициализация сервиса токенов"""
    token_service = TokenService(session=session, _vault_service=vault_service)
    return token_service
