from sqlalchemy import Column, Integer, String, DateTime
from database.database import Base


class TokenModel(Base):
    """Модель токена"""
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    token = Column(String, nullable=False)
    expire = Column(DateTime, nullable=False)
