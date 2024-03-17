from dataclasses import dataclass
from typing import Any
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


@dataclass
class SessionRepository:
    """Класс для сохранения и удаление из БД"""
    session: AsyncSession

    async def session_add(self, save_object):
        """Создание объекта"""
        try:
            self.session.add(instance=save_object)
            await self.session.commit()
            await self.session.refresh(instance=save_object)
            return save_object
        except IntegrityError:
            await self.session.rollback()

    async def session_delete(self, delete_object):
        """Удаление объекта из БД"""
        try:
            await self.session.delete(instance=delete_object)
            await self.session.commit()
            return {"detail": "success deleted."}
        except IntegrityError:
            await self.session.rollback()

    async def session_find_by_parameter(self, model: Any, email: str):
        """Поиск объекта по параметру"""
        data = await self.session.execute(select(model).filter(model.email == email))
        return data.scalar()

    async def session_find_token(self, model: Any, token: str):
        data = await self.session.execute(select(model).filter(model.token == token))
        return data.scalar()
