from dataclasses import dataclass
from src.authorization.schemas import LoginSchemas
from src.registration.models import UserModel
from src.settings.service import SessionService


@dataclass(repr=False, eq=False)
class TokenRepository:
    """Класс для взаимодействия с БД для токенов"""
    login_schemas: LoginSchemas
    session_service: SessionService

    async def find_user_by_email(self):
        """Поиск пользователя по email"""
        user = await self.session_service.get_object_by_parameter(model=UserModel,
                                                                  email=self.login_schemas.email)
        return user

