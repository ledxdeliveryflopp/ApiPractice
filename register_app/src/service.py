from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import UserModel
from src.schemas import UserCreateSchemas
from src.utils import hash_password


async def check_user(session: AsyncSession, username: str, email: EmailStr):
    """Проверка на существование пользователя"""
    user = await session.execute(select(UserModel).filter(or_(UserModel.username == username,
                                                              UserModel.email == email)))
    return user.scalar()


async def create_user(session: AsyncSession, user_schemas: UserCreateSchemas):
    """Создание пользователя"""
    user_check = await check_user(session=session, username=user_schemas.username,
                                  email=user_schemas.email)
    if user_check:
        raise HTTPException(status_code=404, detail="this user already exist")
    else:
        new_user = UserModel(username=user_schemas.username, email=user_schemas.email,
                             password=hash_password(user_schemas.password))
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user
