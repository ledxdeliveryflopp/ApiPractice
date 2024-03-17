from sqlalchemy import Column, String
from src.settings.models import DefaultModel


class Role:
    admin: str = "admin"
    manager: str = "manager"
    user: str = "user"


class UserModel(DefaultModel):
    """Модель пользователей"""
    __tablename__ = "user"

    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False)
    role = Column(String, default=Role.user)
