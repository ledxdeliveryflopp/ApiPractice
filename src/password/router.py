from fastapi import APIRouter, Depends
from src.password.depends import get_password_service
from src.password.schemas import UserBaseSchemas, UserChangePasswordSchemas
from src.password.service import PasswordService

password_router = APIRouter(
    prefix="/reset-password",
    tags=["reset"],
)


@password_router.post('/send-verify-code/')
async def send_code_for_change_password_router(user_schemas: UserBaseSchemas,
                                               code: PasswordService = Depends(get_password_service)):
    return await code.send_code_for_change_password(user_schemas=user_schemas)


@password_router.patch('/change-password/')
async def change_password_router(user_schemas: UserChangePasswordSchemas,
                                 password: PasswordService = Depends(get_password_service)):
    return await password.change_password(user_schemas=user_schemas)
