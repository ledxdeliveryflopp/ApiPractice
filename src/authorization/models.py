from sqlalchemy import Column, String, Integer, DateTime
from src.settings.db import Base


class TokenModel(Base):
    """Модель токенов"""
    __tablename__ = 'token'

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, index=True)
    token = Column(String, nullable=False)
    expire = Column(DateTime, nullable=False)
