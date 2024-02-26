from fastapi import HTTPException, status


class BadCredentials(HTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Incorrect email or password."


class UserExist(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "User already exist."


class UserDontExist(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "User don't exist."
