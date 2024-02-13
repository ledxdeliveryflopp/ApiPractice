from fastapi import FastAPI
from src.authorization.router import authorization_router
from src.registration.router import register_router

authorization = FastAPI()

authorization.include_router(authorization_router)
authorization.include_router(register_router)
