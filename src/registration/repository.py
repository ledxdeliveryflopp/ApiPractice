from dataclasses import dataclass
from sqlalchemy import select
from src.registration.models import UserModel
from src.registration.schemas import UserCreateSchemas
from src.settings.service import SessionService


@dataclass(repr=False, eq=False)
class UserRepository(SessionService):
    """Класс для взаимодействия с БД для пользователей"""

    async def find_user(self, user_schemas: UserCreateSchemas) -> UserModel | None:
        """Поиск пользователя по email"""
        user = await self.session.execute(select(UserModel).filter(UserModel.email ==
                                                                   user_schemas.email))
        return user.scalar()
