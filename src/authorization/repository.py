from dataclasses import dataclass
from starlette.requests import Request
from src.authorization.models import TokenModel
from src.registration.models import UserModel
from src.settings.exceptions import TokenDontExist
from src.settings.service import SessionService


@dataclass(repr=False, eq=False)
class TokenRepository:
    """Класс для взаимодействия с БД для токенов"""
    session_service: SessionService
    request: Request

    async def find_user_by_email(self, email: str):
        """Поиск пользователя по email"""
        user = await self.session_service.get_object_by_parameter(model=UserModel,
                                                                  email=email)
        return user

    async def find_token(self, jwt_token: str):
        """Поиск токена"""
        token = await self.session_service.get_token(model=TokenModel, token=jwt_token)
        if not token:
            raise TokenDontExist
        return token

