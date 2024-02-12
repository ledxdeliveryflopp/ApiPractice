from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas import UserBaseSchemas, UserCreateSchemas
from settings.depends import get_session
from src.service import create_user


router = APIRouter(
    prefix="/register",
    tags=["auth"],
)


@router.post('/register/', response_model=UserBaseSchemas)
async def create_user_router(user_schemas: UserCreateSchemas, session: AsyncSession = Depends(
                             get_session)):
    """Роутер создания пользователя"""
    new_user = await create_user(user_schemas=user_schemas, session=session)
    return new_user
