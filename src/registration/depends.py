from fastapi import Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from src.registration.service import UserService
from src.settings.depends import get_session
from src.vault.service import VaultService, get_vault_service


async def get_user_service(background_tasks: BackgroundTasks,
                           session: AsyncSession = Depends(get_session),
                           vault_service: VaultService = Depends(get_vault_service)):
    """Инициализация сервиса пользователей"""
    user_service = UserService(background_tasks=background_tasks, vault_service=vault_service,
                               session=session)
    return user_service
