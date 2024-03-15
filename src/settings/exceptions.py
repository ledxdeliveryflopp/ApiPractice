from typing import Any
from fastapi import HTTPException, status


class DetailedHTTPException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Server error"

    def __init__(self, **kwargs: dict[str, Any]) -> None:
        super().__init__(status_code=self.status_code, detail=self.detail, **kwargs)


class BadCredentials(DetailedHTTPException):
    """Не верный логин или пароль"""
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Incorrect email or password."


class UserExist(DetailedHTTPException):
    """Пользователь уже существует"""
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "User already exist."


class UserDontExist(DetailedHTTPException):
    """Пользователя не существует"""
    status_code = status.HTTP_404_NOT_FOUND
    detail = "User don't exist."


class VaultInvalidPath(DetailedHTTPException):
    """Не верный путь к секрету в vault"""
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Vault path error, report a problem to technical support."


class VaultInvalidSealed(DetailedHTTPException):
    """Хранилище vault не открыто"""
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Vault sealed, report a problem to technical support."
