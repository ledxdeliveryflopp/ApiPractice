from fastapi import APIRouter, Depends
from src.registration.depends import get_user_service
from src.registration.schemas import UserBaseSchemas
from src.registration.service import UserService

register_router = APIRouter(
    prefix="/registration",
    tags=["auth"],
)


@register_router.post('/register/', response_model=UserBaseSchemas)
async def create_user_router(user: UserService = Depends(get_user_service)):
    """Роутер создания пользователя"""
    return await user.create_user()
