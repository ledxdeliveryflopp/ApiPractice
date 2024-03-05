from dataclasses import dataclass
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.registration.models import UserModel
from src.registration.schemas import UserCreateSchemas
from src.registration.utils import hash_password
from src.settings.exceptions import UserExist
from src.settings.repository import SessionRepository
from src.vault.service import create_secret


@dataclass
class UserRepository:
    """Класс для взаимодействия с БД для пользователей"""
    user_schemas: UserCreateSchemas
    session: AsyncSession

    async def find_user_by_email(self):
        """Поиск пользователя по email"""
        user = await self.session.execute(select(UserModel).filter
                                          ((UserModel.email == self.user_schemas.email)))
        return user.scalar()

    async def create_user(self):
        """Создание пользователя"""
        user = await self.find_user_by_email()
        if user:
            raise UserExist
        user = UserModel(username=self.user_schemas.username, email=self.user_schemas.email)
        await create_secret(email=self.user_schemas.email, password=hash_password(
            password=self.user_schemas.password))
        session_create = SessionRepository(session=self.session, object=user)
        await session_create.session_add()
        return user
