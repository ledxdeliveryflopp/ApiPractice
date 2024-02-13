from pydantic import BaseModel, EmailStr
from datetime import datetime


class TokenBaseSchemas(BaseModel):
    """Основная схема токена"""
    access_token: str
    expire: datetime
    token_type: str


class LoginSchemas(BaseModel):
    """Схема логина"""
    email: EmailStr
    password: str
