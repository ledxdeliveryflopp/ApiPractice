from dataclasses import dataclass
from fastapi import BackgroundTasks
from src.broker.service import send_message_to_broker
from src.registration.repository import UserRepository


@dataclass(repr=False, eq=False)
class UserService:
    """Класс сервиса пользователей"""
    repository: UserRepository
    background_tasks: BackgroundTasks

    async def find_user_by_email(self):
        """Поиск пользователя по email"""
        user = await self.repository.find_user()
        return user

    async def create_user(self):
        """Создание пользователя"""
        new_user = await self.repository.create_user()
        self.background_tasks.add_task(send_message_to_broker, email=f"{new_user.email}")
        return new_user
