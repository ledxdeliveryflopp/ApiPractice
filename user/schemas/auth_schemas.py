from pydantic import BaseModel, EmailStr


class AuthSchemas(BaseModel):
    """Схема аутенфикации"""
    email: EmailStr
    password: str
