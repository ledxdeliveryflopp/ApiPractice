from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from models.user_model import UserModel
from schemas.user_schemas import UserCreateSchemas, UserUpdateSchemas
from utils.user_utils import hash_password


async def get_all_user(session: AsyncSession):
    """Все пользователи"""
    users = await session.execute(Select(UserModel))
    if not users:
        raise HTTPException(status_code=404, detail="not found")
    else:
        return users.scalars().all()


async def get_user_by_id(session: AsyncSession, id: int):
    """Пользователь по id"""
    user = await session.execute(Select(UserModel).filter(UserModel.id == id))
    return user.scalar()


async def get_user_by_email(session: AsyncSession, email: EmailStr):
    """Пользователь по email"""
    user = await session.execute(Select(UserModel).filter(UserModel.email == email))
    return user.scalar()


async def create_user(session: AsyncSession, user_schemas: UserCreateSchemas):
    """Создание пользователя"""
    user_check = await get_user_by_email(session=session, email=user_schemas.email)
    if user_check:
        raise HTTPException(status_code=404, detail="this user already exist")
    else:
        new_user = UserModel(email=user_schemas.email,
                             password=hash_password(password=user_schemas.password))
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user


async def update_user(session: AsyncSession, user_id: int, user_schemas: UserUpdateSchemas):
    """Обновление пользователя"""
    user = await get_user_by_id(session=session, id=user_id)
    if not user:
        return HTTPException(status_code=404, detail="not found")
    else:
        for var, value in vars(user_schemas).items():
            setattr(user, var, value) if value else None
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

