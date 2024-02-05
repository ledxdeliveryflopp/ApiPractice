from sqlalchemy import Column, Integer, String
from user_database.database import Base


class UserModel(Base):
    """Модель пользователей"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, unique=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
