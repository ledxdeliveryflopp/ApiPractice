import random
import os
import string
from datetime import timedelta, datetime
from dotenv import load_dotenv
from fastapi import HTTPException, Request
from jose import jwt
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from crud.user_crud import get_user_by_email
from models.token_models import TokenModel
from schemas.auth_schemas import AuthSchemas
from utils.user_utils import verify_password

load_dotenv()

secret_key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")


async def create_access_token(session: AsyncSession, user_email: str):
    """Создание access токена"""
    data = {}
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=15)
    expire_str = expire.strftime("%d-%m-%Y %H:%M:%S")
    random_string = random.choices(string.ascii_letters, k=10)
    to_encode.update({"expire": expire_str, "user_email": user_email, "random": random_string,
                     "token_type": "bearer"})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    new_token = TokenModel(token=encoded_jwt, expire=expire)
    session.add(new_token)
    await session.commit()
    await session.refresh(new_token)
    return new_token


async def login(session: AsyncSession, login_schemas: AuthSchemas):
    """Авторизация"""
    user = await get_user_by_email(session=session, email=login_schemas.email)
    password = await verify_password(plain_password=login_schemas.password, password=user.password)
    if not user or not password:
        raise HTTPException(status_code=400, detail="incorrect email or password")
    else:
        access_token = await create_access_token(session=session, user_email=login_schemas.email)
        return {"access_token": access_token.token, "token_type": "Bearer"}


async def get_token(session: AsyncSession, token: str):
    """Получить токен"""
    token = await session.execute(Select(TokenModel).filter(TokenModel.token == token))
    if token:
        return token.scalar()
    else:
        return HTTPException(status_code=404, detail="not found")


async def verify_token(session: AsyncSession, request: Request):
    """Проверка токена"""
    try:
        request.headers["Authorization"]
    except KeyError:
        raise HTTPException(status_code=401, detail="empty Authorization header")
    header_token = request.headers
    header_token = header_token.get('authorization')
    header_token = str(header_token)
    header_token = header_token.replace("Bearer ", '')
    token = await get_token(session=session, token=header_token)
    if not token:
        raise HTTPException(status_code=401, detail="token dont exist")
    elif token.expire < datetime.now():
        await session.delete(token)
        await session.commit()
        raise HTTPException(status_code=401, detail="token overdue")
    else:
        return token
