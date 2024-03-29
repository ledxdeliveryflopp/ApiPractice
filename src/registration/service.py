from dataclasses import dataclass
from fastapi import BackgroundTasks
from src.broker.service import send_message_to_broker
from src.registration.models import UserModel
from src.registration.repository import UserRepository
from src.registration.schemas import UserCreateSchemas
from src.registration.utils import hash_password
from src.settings.exceptions import UserExist
from src.vault.service import VaultService


@dataclass(repr=False, eq=False)
class UserService(UserRepository):
    """Класс сервиса пользователей"""
    vault_service: VaultService
    background_tasks: BackgroundTasks

    async def find_user_by_email(self, user_schemas: UserCreateSchemas) -> UserModel:
        """Поиск пользователя по email"""
        user = await self.find_user(user_schemas=user_schemas)
        return user

    async def create_user(self, user_schemas: UserCreateSchemas) -> UserModel:
        user = await self.find_user(user_schemas=user_schemas)
        if user:
            raise UserExist
        new_user = UserModel(username=user_schemas.username, email=user_schemas.email)
        await self.create_object(save_object=new_user)
        await self.vault_service.create_secret(user_id=new_user.id, password=hash_password(
                                               user_schemas.password))
        self.background_tasks.add_task(send_message_to_broker, email=f"{new_user.email}")
        return new_user
