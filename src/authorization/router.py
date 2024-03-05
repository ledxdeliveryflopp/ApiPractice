from fastapi import APIRouter, Depends
from src.authorization.depends import get_token_service
from src.authorization.schemas import TokenBaseSchemas
from src.authorization.service import TokenService


authorization_router = APIRouter(
    prefix="/authorization",
    tags=["auth"],
)


@authorization_router.post('/login/', response_model=TokenBaseSchemas)
async def login_router(token: TokenService = Depends(get_token_service)):
    """Роутер авторизации"""
    new_token = await token.login()
    return new_token
