from pydantic import BaseModel, EmailStr, Field


class UserBaseSchemas(BaseModel):
    """базовая схема пользователя"""
    email: EmailStr


class UserChangePasswordSchemas(BaseModel):
    """Схема сброса пароля"""

    code: str = Field(min_length=32)
    password: str = Field(min_length=6)
