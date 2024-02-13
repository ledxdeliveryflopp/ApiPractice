from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.authorization.schemas import TokenBaseSchemas, LoginSchemas
from src.authorization.service import login
from src.settings.depends import get_session


authorization_router = APIRouter(
    prefix="/authorization",
    tags=["auth"],
)


@authorization_router.post('/login/', response_model=TokenBaseSchemas)
async def login_router(login_schemas: LoginSchemas, session: AsyncSession = Depends(get_session)):
    """Роутер авторизации"""
    token = await login(session=session, login_schemas=login_schemas)
    return token
