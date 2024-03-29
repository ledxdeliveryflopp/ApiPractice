from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.settings.db import async_session
from src.settings.service import SessionService


async def get_session():
    async with async_session() as session:
        yield session


async def get_session_service(session: AsyncSession = Depends(get_session)):
    project_service = SessionService(session=session)
    return project_service
