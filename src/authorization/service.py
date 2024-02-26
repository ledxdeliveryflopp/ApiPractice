import random
import string
from datetime import datetime, timedelta
from jose import jwt
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.authorization.models import TokenModel
from src.authorization.schemas import LoginSchemas
from src.authorization.utils import verify_password
from src.registration.models import UserModel
from src.settings.exceptions import BadCredentials
from src.settings.settings import Settings
from src.vault.service import read_secret

settings = Settings()


async def get_user_by_email(session: AsyncSession, email: EmailStr):
    """Пользователь по email"""
    user = await session.execute(select(UserModel).filter(UserModel.email == email))
    return user.scalar()


async def create_access_token(session: AsyncSession, user_email: EmailStr):
    """Создание токена"""
    data = {}
    expire = datetime.now() + timedelta(minutes=15)
    expire_str = expire.strftime("%d-%m-%Y %H:%M:%S")
    random_string = random.choices(string.ascii_letters, k=4)
    data.update({"expire": expire_str, "user_email": user_email, "random": random_string,
                 "token_type": "bearer"})
    encoded_jwt = jwt.encode(data, settings.secret_key, algorithm=settings.algorithm)
    new_token = TokenModel(token=encoded_jwt, expire=expire)
    session.add(new_token)
    await session.commit()
    await session.refresh(new_token)
    return new_token


async def login(session: AsyncSession, login_schemas: LoginSchemas):
    """Авторизация"""
    user = await get_user_by_email(session=session, email=login_schemas.email)
    if not user:
        raise BadCredentials
    password_from_vault = await read_secret(email=login_schemas.email)
    password = await verify_password(plain_password=login_schemas.password,
                                     password=password_from_vault)
    if not password:
        raise BadCredentials
    else:
        access_token = await create_access_token(session=session, user_email=login_schemas.email)
        return {"access_token": access_token.token, "token_type": "Bearer"}
