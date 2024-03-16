from dataclasses import dataclass
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from src.registration.models import UserModel
from src.registration.schemas import UserCreateSchemas
from src.registration.utils import hash_password
from src.settings.exceptions import UserExist
from src.settings.repository import SessionRepository
from src.vault.repository import VaultRepository


@dataclass(repr=False, eq=False)
class UserRepository:
    """Класс для взаимодействия с БД для пользователей"""
    user_schemas: UserCreateSchemas
    session: AsyncSession

    async def find_user(self):
        """Поиск пользователя по email"""
        user = await self.session.execute(select(UserModel).filter
                                          (or_(UserModel.email == self.user_schemas.email,
                                               UserModel.username == self.user_schemas.username)))
        return user.scalar()

    async def create_user(self):
        """Создание пользователя"""
        user = await self.find_user()
        if user:
            raise UserExist
        user = UserModel(username=self.user_schemas.username, email=self.user_schemas.email)
        vault_repository = VaultRepository()
        session_create = SessionRepository(session=self.session, object=user)
        await session_create.session_add()
        await vault_repository.create_secret(user_id=user.id,
                                             password=hash_password(self.user_schemas.password))
        return user
