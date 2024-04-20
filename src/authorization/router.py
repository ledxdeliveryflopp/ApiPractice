from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from src.authorization.depends import get_token_service
from src.authorization.schemas import TokenBaseSchemas, LoginSchemas
from src.authorization.service import TokenService


authorization_router = APIRouter(
    prefix="/authorization",
    tags=["auth"],
)


bearer_token = HTTPBearer()


@authorization_router.post('/login/', response_model=TokenBaseSchemas)
async def login_router(login_schemas: LoginSchemas, token_service: TokenService = Depends(
                       get_token_service)) -> dict:
    """Роутер авторизации"""
    return await token_service.login(login_schemas=login_schemas)
