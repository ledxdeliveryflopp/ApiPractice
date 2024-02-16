from pydantic import EmailStr
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from src.registration.models import UserModel
from src.registration.schemas import UserCreateSchemas
from src.registration.utils import hash_password
from src.registration.vault import create_secret
from src.settings.exceptions import UserExist


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
        raise UserExist
    else:
        new_user = UserModel(username=user_schemas.username, email=user_schemas.email)
        user_password = create_secret()
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user
