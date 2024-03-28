import random
import string
from dataclasses import dataclass
from src.broker.service import send_reset_code_to_broker
from src.password.models import EmailCode
from src.password.repository import PasswordRepository
from src.password.schemas import UserBaseSchemas, UserChangePasswordSchemas
from src.registration.utils import hash_password
from src.settings.exceptions import UserDontExist, BadCode, BadVerifyToken
import uuid
from src.settings.service import SessionService
from src.vault.service import VaultService


@dataclass
class PasswordService:
    password_repository: PasswordRepository
    session_service: SessionService

    async def send_code_for_change_password(self, user_schemas: UserBaseSchemas):
        """Отправить код для подтверждения смены пароля"""
        user = await self.password_repository.get_user_by_email(email=user_schemas.email)
        if not user:
            raise UserDontExist
        code = uuid.uuid4()
        code_in_db = EmailCode(title=code, user_email=user.email)
        letters = string.ascii_letters
        password = ''.join(random.choice(letters) for i in range(9))
        vault = VaultService()
        await vault.create_secret(user_id=user.id, password=hash_password(password=password))
        await send_reset_code_to_broker(data={"code": f"{code}", "email": f"{user.email}",
                                              "timed_password": f"{password}"})
        await self.session_service.create_object(save_object=code_in_db)
        return {"detail": f"Code send to {user.email}"}

    async def change_password(self, user_schemas: UserChangePasswordSchemas):
        """Проверить код и сменить пароль"""
        code = await self.password_repository.find_code(code=user_schemas.code)
        if not code:
            raise BadCode
        user = await self.password_repository.find_user_by_code(code_email=code.user_email)
        if not user:
            raise UserDontExist
        if code.user_email != user.email:
            raise BadVerifyToken
        vault = VaultService()
        new_password = user_schemas.password
        await vault.create_secret(user_id=user.id, password=hash_password(password=new_password))
        await self.session_service.delete_object(delete_object=code)
        return {"detail": "Success"}
