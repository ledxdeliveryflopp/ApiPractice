from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from crud.user_crud import get_all_user, create_user, update_user, get_user_by_email
from database.database import async_session
from schemas.user_schemas import UserBaseSchemas, UserCreateSchemas, UserUpdateSchemas

user = FastAPI()


async def get_session():
    session = async_session()
    try:
        yield session
    finally:
        await session.close()


@user.get('/all-user/', response_model=list[UserBaseSchemas])
async def get_all_user_router(session: AsyncSession = Depends(get_session)):
    """Роутер вывода всех пользователей"""
    users = await get_all_user(session=session)
    return users


@user.post('/create-user/', response_model=UserBaseSchemas)
async def create_user_router(user_schemas: UserCreateSchemas,
                             session: AsyncSession = Depends(get_session)):
    """Роутер создания пользователя"""
    new_user = await create_user(user_schemas=user_schemas, session=session)
    return new_user


@user.patch('/update-user/{user_id}', response_model=UserBaseSchemas)
async def update_user_router(user_schemas: UserUpdateSchemas, user_id: int, session: AsyncSession
                             = Depends(get_session)):
    """Обновление пользователя"""
    updated_user = await update_user(user_schemas=user_schemas, user_id=user_id, session=session)
    return updated_user
