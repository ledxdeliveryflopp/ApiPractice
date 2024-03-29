from dataclasses import dataclass
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from src.authorization.models import TokenModel
from src.registration.models import UserModel
from src.settings.exceptions import TokenDontExist


@dataclass(repr=False, eq=False)
class TokenRepository:
    """Класс для взаимодействия с БД для токенов"""
    session: AsyncSession
    request: Request

    async def find_user_by_email(self, email: str) -> UserModel:
        """Поиск пользователя по email"""
        user = await self.session.execute(select(UserModel).filter(UserModel.email == email))
        return user.scalar()

    async def find_token(self, jwt_token: str) -> TokenModel:
        """Поиск токена"""
        token = await self.session.execute(select(TokenModel).filter(TokenModel.token == jwt_token))
        if not token:
            raise TokenDontExist
        return token

