from dataclasses import dataclass
from datetime import datetime, timedelta
import random
import string
from jose import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.authorization.models import TokenModel
from src.authorization.schemas import LoginSchemas
from src.authorization.utils import verify_password
from src.registration.models import UserModel
from src.settings.exceptions import BadCredentials
from src.settings.repository import SessionRepository
from src.settings.settings import settings
from src.vault.repository import VaultRepository


@dataclass(repr=False, eq=False)
class TokenRepository:
    """Класс для взаимодействия с БД для токенов"""
    login_schemas: LoginSchemas
    session: AsyncSession

    async def find_user_by_email(self):
        """Поиск пользователя по email"""
        user = await self.session.execute(select(UserModel).filter
                                          ((UserModel.email == self.login_schemas.email)))
        return user.scalar()

    async def create_access_token(self):
        """Создание access токена"""
        data = {}
        expire = datetime.now() + timedelta(minutes=15)
        expire_str = expire.strftime("%d-%m-%Y %H:%M:%S")
        random_string = random.choices(string.ascii_letters, k=4)
        data.update({"expire": expire_str, "user_email": self.login_schemas.email, "random":
                    random_string, "token_type": "bearer"})
        encoded_jwt = jwt.encode(data, settings.jwt_settings.jwt_secret,
                                 algorithm=settings.jwt_settings.jwt_algorithm)
        new_token = TokenModel(token=encoded_jwt, expire=expire)
        session_create = SessionRepository(session=self.session, object=new_token)
        await session_create.session_add()
        return new_token

    async def login(self):
        """Авторизация"""
        user = await self.find_user_by_email()
        if not user:
            raise BadCredentials
        vault_repository = VaultRepository()
        password_from_vault = await vault_repository.read_secret(email=self.login_schemas.email)
        password = await verify_password(plain_password=self.login_schemas.password,
                                         password=password_from_vault)
        if not password:
            raise BadCredentials
        access_token = await self.create_access_token()
        return {"access_token": access_token.token, "token_type": "Bearer"}
