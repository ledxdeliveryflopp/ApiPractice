from dataclasses import dataclass
from src.registration.models import UserModel
from src.registration.schemas import UserCreateSchemas
from src.registration.utils import hash_password
from src.settings.service import SessionService
from src.vault.service import VaultService


@dataclass(repr=False, eq=False)
class UserRepository:
    """Класс для взаимодействия с БД для пользователей"""
    user_schemas: UserCreateSchemas
    session_service: SessionService

    async def find_user(self):
        """Поиск пользователя по email"""
        user = await self.session_service.get_object_by_parameter(model=UserModel,
                                                                  email=self.user_schemas.email)
        return user

    async def create_user(self):
        new_user = UserModel(username=self.user_schemas.username, email=self.user_schemas.email)
        await self.session_service.create_object(save_object=new_user)
        await self.session_service.create_object(save_object=new_user)
        vault_service = VaultService()
        await vault_service.create_secret(user_id=new_user.id,
                                          password=hash_password(self.user_schemas.password))
        return new_user
