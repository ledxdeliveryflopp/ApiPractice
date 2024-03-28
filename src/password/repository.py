from dataclasses import dataclass
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from src.password.models import EmailCode
from src.registration.models import UserModel
from src.settings.exceptions import UserDontExist, BadCode


@dataclass
class PasswordRepository:
    session: AsyncSession

    async def get_user_by_email(self, email: str):
        """Получить пользователя по Email"""
        user = await self.session.execute(Select(UserModel).filter(UserModel.email == email))
        if not user:
            raise UserDontExist
        return user.scalar()

    async def find_code(self, code: str):
        """Функция поиска кода сброса"""
        code_db = await self.session.execute(Select(EmailCode).filter(EmailCode.title == code))
        if not code_db:
            raise BadCode
        return code_db.scalar()

    async def find_user_by_code(self, code_email: str):
        """Поиск пользователя по коду сброса"""
        user = await self.session.execute(Select(UserModel).filter(UserModel.email == code_email))
        if not user:
            raise UserDontExist
        return user.scalar()
