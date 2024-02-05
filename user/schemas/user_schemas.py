from pydantic import BaseModel, EmailStr, Field


class UserBaseSchemas(BaseModel):
    """Основная схема пользователя"""
    email: EmailStr


class UserCreateSchemas(UserBaseSchemas):
    """Схема создания пользователя"""
    password: str = Field(ge=6)


class UserUpdateSchemas(UserBaseSchemas):
    """Схема обновления пользователя"""
    pass
