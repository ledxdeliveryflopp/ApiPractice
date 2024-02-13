from pydantic import BaseModel, EmailStr


class TokenBaseSchemas(BaseModel):
    """Основная схема токена"""
    access_token: str
    expire: str
    token_type: str


class LoginSchemas(BaseModel):
    """Схема логина"""
    email: EmailStr
    password: str
