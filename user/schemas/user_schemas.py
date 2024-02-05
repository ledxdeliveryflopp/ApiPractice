from pydantic import BaseModel, EmailStr, Field


class UserBaseSchemas(BaseModel):
    """Основная схема пользователя"""
    email: EmailStr


class UserCreateSchemas(UserBaseSchemas):
    """Схема создания пользователя"""
    password: str = Field(min_length=8)


class UserUpdateSchemas(UserBaseSchemas):
    """Схема обновления пользователя"""
    pass
