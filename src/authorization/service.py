from dataclasses import dataclass
from src.authorization.repositroy import TokenRepository


@dataclass(repr=False)
class TokenService:
    """Класс сервиса токенов"""
    repository: TokenRepository

    async def create_access_token(self):
        """Создание access токена"""
        new_access_token = await self.repository.create_access_token()
        return new_access_token

    async def login(self):
        """Авторизация"""
        user = await self.repository.login()
        return user
