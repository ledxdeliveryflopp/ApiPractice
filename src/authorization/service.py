import random
import string
from dataclasses import dataclass
from datetime import datetime, timedelta
from jose import jwt
from src.authorization.models import TokenModel
from src.authorization.repository import TokenRepository
from src.authorization.schemas import LoginSchemas
from src.authorization.utils import verify_password
from src.settings.exceptions import BadCredentials
from src.settings.settings import settings
from src.vault.service import VaultService


@dataclass(repr=False, eq=False)
class TokenService(TokenRepository):
    """Класс сервиса токенов"""
    _vault_service: VaultService

    async def create_access_token(self, user_role: str, email: str) -> TokenModel:
        """Создание access токена"""
        data = {}
        expire = datetime.utcnow() + timedelta(minutes=30)
        random_string = random.choices(string.printable, k=10)
        data.update({"user_email": email, "user_role": user_role,
                     "random": random_string, "token_type": "bearer"})
        encoded_jwt = jwt.encode(data, settings.jwt_settings.jwt_secret,
                                 algorithm=settings.jwt_settings.jwt_algorithm)
        new_token = TokenModel(token=encoded_jwt, expire=expire)
        await self.create_object(save_object=new_token)
        return new_token

    async def login(self, login_schemas: LoginSchemas) -> dict:
        """Авторизация"""
        user = await self.find_user_by_email(email=login_schemas.email)
        if not user:
            raise BadCredentials
        password_from_vault = await self._vault_service.read_secret(user_id=user.id)
        password = await verify_password(plain_password=login_schemas.password,
                                         password=password_from_vault)
        if not password:
            raise BadCredentials
        access_token = await self.create_access_token(email=login_schemas.email,
                                                      user_role=user.role)
        return {"access_token": access_token.token, "token_type": "Bearer"}
