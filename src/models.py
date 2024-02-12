from sqlalchemy import Column, String
from src.settings.models import DefaultModel


class UserModel(DefaultModel):
    """Модель пользователей"""
    __tablename__ = "user"

    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

