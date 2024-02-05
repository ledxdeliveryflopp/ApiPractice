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
        update_data = user_schemas.dict(exclude_unset=True)
        updated_user = user.copy(update=update_data)
        session.add(updated_user)
        await session.commit()
        await session.refresh(updated_user)
        return updated_user
