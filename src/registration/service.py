from dataclasses import dataclass
from src.registration.repository import UserRepository


@dataclass(repr=False, eq=False)
class UserService:
    """Класс сервиса пользователей"""
    repository: UserRepository

    async def create_user(self):
        """Создание пользователя"""
        new_user = await self.repository.create_user()
        return new_user

    async def find_user_by_email(self):
        """Поиск пользователя по email"""
        user = await self.repository.find_user()
        return user
