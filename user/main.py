from fastapi import FastAPI, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from crud.auth_crud import login, verify_token
from crud.user_crud import get_all_user, create_user, update_user
from database.database import async_session
from schemas.auth_schemas import AuthSchemas
from schemas.user_schemas import UserBaseSchemas, UserCreateSchemas, UserUpdateSchemas


user = FastAPI()


async def get_session():
    session = async_session()
    try:
        yield session
    finally:
        await session.close()


@user.get('/all-user/', response_model=list[UserBaseSchemas])
async def get_all_user_router(request: Request, session: AsyncSession = Depends(get_session)):
    """Роутер вывода всех пользователей"""
    token = await verify_token(session=session, request=request)
    if token:
        users = await get_all_user(session=session)
        return users
    else:
        return token


@user.post('/create-user/', response_model=UserBaseSchemas)
async def create_user_router(user_schemas: UserCreateSchemas,
                             session: AsyncSession = Depends(get_session)):
    """Роутер создания пользователя"""
    new_user = await create_user(user_schemas=user_schemas, session=session)
    return new_user


@user.patch('/update-user/{user_id}', response_model=UserBaseSchemas)
async def update_user_router(user_schemas: UserUpdateSchemas, user_id: int, session: AsyncSession
                             = Depends(get_session)):
    """Роутер обновления пользователя"""
    updated_user = await update_user(user_schemas=user_schemas, user_id=user_id, session=session)
    return updated_user


@user.post('/login/')
async def login_router(login_schemas: AuthSchemas, session: AsyncSession = Depends(get_session)):
    """Роутер авторизации"""
    access_token = await login(session=session, login_schemas=login_schemas)
    return access_token
