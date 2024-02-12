from pydantic import BaseModel, EmailStr, Field


class UserBaseSchemas(BaseModel):
    """Основная схема пользователя"""
    username: str = Field(min_length=4)
    email: EmailStr


class UserCreateSchemas(UserBaseSchemas):
    """Схема создания пользователя"""
    password: str = Field(min_length=8)

