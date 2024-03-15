from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class SessionRepository:
    """Класс для сохранения и удаление из БД"""
    session: AsyncSession
    object: dict

    async def session_add(self):
        """Запись объекта в БД"""
        self.session.add(instance=self.object)
        await self.session.commit()
        await self.session.refresh(instance=self.object)

    async def session_delete(self):
        """Удаление объекта из БД"""
        await self.session.delete(instance=self.object)
        await self.session.commit()
