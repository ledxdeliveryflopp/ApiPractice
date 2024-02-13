from typing import Any
from fastapi import HTTPException, status


class DetailedHTTPException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Server error"

    def __init__(self, **kwargs: dict[str, Any]) -> None:
        super().__init__(status_code=self.status_code, detail=self.detail, **kwargs)


class BadCredentials(DetailedHTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Incorrect email or password."


class UserExist(DetailedHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "User already exist."
